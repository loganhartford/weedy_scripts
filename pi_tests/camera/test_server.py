from http.server import BaseHTTPRequestHandler, HTTPServer

class TestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, world!")

def run(server_class=HTTPServer, handler_class=TestHandler, port=8000):
    server_address = ('0.0.0.0', port)  # Listen on all interfaces
    httpd = server_class(server_address, handler_class)
    print(f"Starting test server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
