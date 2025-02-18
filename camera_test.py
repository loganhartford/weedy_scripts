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
    "AnalogueGain": 2,          # Let the camera control ISO dynamically
    # "AwbEnable": True,          # Auto white balance enabled
    # "AwbMode": 1,               # Auto white balance mode
})

picam2.start()

# Capture an image and save it as a JPEG file
image_stream = BytesIO()
picam2.capture_file(image_stream, format='jpeg')
image_stream.seek(0)

with open('/home/weedy/weedy_scripts/captured_image.jpg', 'wb') as f:
    f.write(image_stream.read())

picam2.close()
print("Image captured and saved as captured_image.jpg")
