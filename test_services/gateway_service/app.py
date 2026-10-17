
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json
import os


USER_SERVICE_URL = os.getenv(
    "USER_SERVICE_URL",
    "http://localhost:8000"
)


class GatewayHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code, data):
        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )

    def do_GET(self):

        if self.path == "/health":
            self.send_json(
                200,
                {"status": "healthy"}
            )
            return

        if self.path == "/api/status":
            self.send_json(
                200,
                {"service": "gateway", "status": "healthy"}
            )
            return

        if self.path.startswith("/api/user/"):

            user_id = self.path.split("/")[-1]

            user_url = (
                f"{USER_SERVICE_URL}/users/{user_id}"
            )

            try:
                with urlopen(user_url, timeout=3) as response:
                    user_data = json.loads(
                        response.read().decode("utf-8")
                    )

                self.send_json(
                    200,
                    {
                        "source": "gateway",
                        "user": user_data
                    }
                )

            except HTTPError as error:
                if error.code == 400:
                    self.send_json(
                        400,
                        {"error": "Invalid user ID"}
                    )

                elif error.code == 404:
                    self.send_json(
                        404,
                        {"error": "User not found"}
                    )

                else:
                    self.send_json(
                        502,
                        {"error": "User service returned an error"}
                    )

            except (URLError, TimeoutError):
                self.send_json(
                    502,
                    {"error": "User service unavailable"}
                )

            return

        self.send_json(
            404,
            {"error": "Endpoint not found"}
        )


GATEWAY_PORT = int(
    os.getenv("GATEWAY_PORT", "8001")
)

server = HTTPServer(
    ("0.0.0.0", GATEWAY_PORT),
    GatewayHandler
)

print(f"Gateway Service running on port {GATEWAY_PORT}")

server.serve_forever()
