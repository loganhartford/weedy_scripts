from http.server import BaseHTTPRequestHandler, HTTPServer
from picamera2 import Picamera2
from io import BytesIO
import time

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)

# Autofocus, Auto Exposure, and Dynamic ISO Range
picam2.set_controls({
    "AfMode": 1,                # Autofocus mode enabled
    "AeEnable": True,           # Auto exposure enabled
    "AeMeteringMode": 1,        # Center-weighted metering for balanced exposure
    "ExposureTime": 0,          # Set to 0 for auto exposure (let the camera decide)
    "AnalogueGain": 0,          # Let the camera control ISO dynamically
    # "AwbEnable": True,          # Auto white balance enabled
    # "AwbMode": 1,               # Auto white balance mode
})

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
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    try:
        run()
    except:
        picam2.close()
        print(f"Camera closed")
