from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


class EventHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        length = int(
            self.headers["Content-Length"]
        )

        body = self.rfile.read(length)

        print("\nReceived event:")
        print(body.decode())


        self.send_response(200)
        self.end_headers()



server = HTTPServer(
    ("0.0.0.0", 8000),
    EventHandler
)


print("Mock SIEM server running...")

server.serve_forever()