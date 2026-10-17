
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


USERS = {
    1: {
        "id": 1,
        "name": "Hariharan"
    },
    2: {
        "id": 2,
        "name": "Arun"
    }
}


class UserServiceHandler(BaseHTTPRequestHandler):

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

        if self.path.startswith("/users/"):

            user_id_text = self.path.split("/")[-1]

            try:
                user_id = int(user_id_text)
            except ValueError:
                self.send_json(
                    400,
                    {"error": "Invalid user ID"}
                )
                return

            user = USERS.get(user_id)

            if user is None:
                self.send_json(
                    404,
                    {"error": "User not found"}
                )
                return

            self.send_json(200, user)
            return

        self.send_json(
            404,
            {"error": "Endpoint not found"}
        )


server = HTTPServer(
    ("0.0.0.0", 8000),
    UserServiceHandler
)

print("User Service running on port 8000")

server.serve_forever()
