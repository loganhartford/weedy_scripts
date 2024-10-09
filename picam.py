#!/usr/bin/python3
from picamera2 import Picamera2

# Create a Picamera2 instance
picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)

# Start the camera
picam2.start()

# Capture an image and save it to a file
picam2.capture_file("captured_image.jpg")

# Stop the camera
picam2.stop()

print("Image captured and saved as captured_image.jpg")
