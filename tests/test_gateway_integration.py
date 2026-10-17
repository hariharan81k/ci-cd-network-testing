
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
