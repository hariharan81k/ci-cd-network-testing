import os
import socket
import subprocess
import sys
import time
from pathlib import Path
import json
from urllib.error import HTTPError
from urllib.request import urlopen


def test_gateway_can_retrieve_user():
    url = "http://localhost:8001/api/user/1"

    with urlopen(url, timeout=5) as response:
        status_code = response.status
        response_data = json.loads(
            response.read().decode("utf-8")
        )

    assert status_code == 200
    assert response_data["source"] == "gateway"
    assert response_data["user"]["id"] == 1
    assert response_data["user"]["name"] == "Hariharan"


def test_gateway_returns_400_for_invalid_user_id():
    url = "http://localhost:8001/api/user/abc"

    try:
        urlopen(url, timeout=5)
        assert False, "Expected HTTP 400"
    except HTTPError as error:
        assert error.code == 400

        response_data = json.loads(
            error.read().decode("utf-8")
        )

        assert response_data["error"] == "Invalid user ID"


def test_gateway_returns_404_for_missing_user():
    url = "http://localhost:8001/api/user/999"

    try:
        urlopen(url, timeout=5)
        assert False, "Expected HTTP 404"
    except HTTPError as error:
        assert error.code == 404

        response_data = json.loads(
            error.read().decode("utf-8")
        )

        assert response_data["error"] == "User not found"


def test_user_service_health():
    url = "http://localhost:8000/health"

    with urlopen(url, timeout=5) as response:
        response_data = json.loads(
            response.read().decode("utf-8")
        )

    assert response.status == 200
    assert response_data["status"] == "healthy"


def test_gateway_health():
    url = "http://localhost:8001/health"

    with urlopen(url, timeout=5) as response:
        response_data = json.loads(
            response.read().decode("utf-8")
        )

    assert response.status == 200
    assert response_data["status"] == "healthy"

def test_gateway_returns_502_when_user_service_is_unavailable():
    # Reserve an unused local port, then release it.
    with socket.socket() as temporary_socket:
        temporary_socket.bind(("127.0.0.1", 0))
        unavailable_port = temporary_socket.getsockname()[1]

    # Find an unused port for the temporary Gateway Service.
    with socket.socket() as temporary_socket:
        temporary_socket.bind(("127.0.0.1", 0))
        gateway_port = temporary_socket.getsockname()[1]

    project_root = Path(__file__).resolve().parents[1]
    gateway_script = (
        project_root
        / "test_services"
        / "gateway_service"
        / "app.py"
    )

    environment = os.environ.copy()
    environment["USER_SERVICE_URL"] = (
        f"http://127.0.0.1:{unavailable_port}"
    )
    environment["GATEWAY_PORT"] = str(gateway_port)

    gateway_process = subprocess.Popen(
        [sys.executable, str(gateway_script)],
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        # Wait until the temporary Gateway Service is ready.
        gateway_url = f"http://127.0.0.1:{gateway_port}/api/user/1"

        for _ in range(30):
            if gateway_process.poll() is not None:
                raise RuntimeError("Temporary Gateway Service stopped unexpectedly")

            try:
                with urlopen(
                    f"http://127.0.0.1:{gateway_port}/health",
                    timeout=1,
                ):
                    break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("Temporary Gateway Service did not start")

        try:
            urlopen(gateway_url, timeout=5)
            assert False, "Expected HTTP 502"
        except HTTPError as error:
            assert error.code == 502

            response_data = json.loads(
                error.read().decode("utf-8")
            )

            assert response_data["error"] == "User service unavailable"

    finally:
        gateway_process.terminate()
        try:
            gateway_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            gateway_process.kill()
            gateway_process.wait()