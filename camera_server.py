from http.server import BaseHTTPRequestHandler, HTTPServer
from picamera2 import Picamera2
from io import BytesIO
import time

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)

# Autofocus, Auto Exposure, and Dynamic ISO Range
# Modified controls for shooting on the move
picam2.set_controls({
    "AfMode": 2,                # Hypothetical continuous autofocus mode (check docs for exact value)
    "AeEnable": True,           # Auto exposure enabled
    "AeMeteringMode": 1,        # Try different modes if needed (e.g., 1 for center-weighted)
    "ExposureTime": 6000,       # Fixed short exposure time in microseconds
    "AnalogueGain": 4,          # Increase gain to compensate for reduced exposure; adjust as needed
    # "AwbEnable": True,        # Optionally enable auto white balance if lighting conditions vary
})

picam2.start()

picam2.start()

class CameraHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Capture an image
        image_stream = BytesIO()
        picam2.capture_file(image_stream, format='jpeg')
        image_stream.seek(0)
        
        # Send the response
        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(image_stream.read())
        

# Start the HTTP server
def run(server_class=HTTPServer, handler_class=CameraHandler, port=8000):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run()
    except:
        picam2.close()
        print(f"Camera closed")
