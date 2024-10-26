from http.server import BaseHTTPRequestHandler, HTTPServer
from picamera2 import Picamera2
from io import BytesIO
import time

class CameraHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Start the camera
        picam2 = Picamera2()
        picam2.start()
        time.sleep(2)  # Allow the camera to warm up

        # Capture an image
        image_stream = BytesIO()
        picam2.capture_file(image_stream, format='jpeg')
        image_stream.seek(0)
        
        # Send the response
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(image_stream.read())
        picam2.close()

# Start the HTTP server
def run(server_class=HTTPServer, handler_class=CameraHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
