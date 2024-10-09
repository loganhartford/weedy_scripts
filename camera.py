#!/usr/bin/python3
from RPi import GPIO
from datetime import datetime
import time
from picamera2 import Picamera2

GPIO.setmode(GPIO.BCM)

# GPIO setup
button_pin = 17
red_pin = 27
green_pin = 22
GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# Initialize Picamera2
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
# picam2.set_controls({   "ExposureTime": 20000, 
#                         "AnalogueGain": 1.0, 
#                         "AwbEnable": False,         # Disable auto white balance for consistency
#                         "AfMode": 1})               # Autofocus mode
picam2.set_controls({ "AfMode": 1})                     # Autofocus mode

picam2.start()

def capture_image():
    try:
        filename = f"img/captured_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        picam2.capture_file(filename)
        print(f"Image captured: {filename}")
        return 0
    except Exception as e:
        print(f"Error capturing image: {e}")
        return -1

try:
    for i in range(3):
        GPIO.output(green_pin, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(green_pin, GPIO.LOW)
        time.sleep(0.3)
    while True:
        if (GPIO.input(button_pin) == GPIO.HIGH):
            ret = capture_image()
            if ret:
                GPIO.output(red_pin, GPIO.HIGH)
            else:
                GPIO.output(green_pin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(red_pin, GPIO.LOW)
            GPIO.output(green_pin, GPIO.LOW)

            # Exit the loop if the button is held for the duration of the status LED
            if (GPIO.input(button_pin) == GPIO.HIGH):
                for i in range(3):
                    GPIO.output(red_pin, GPIO.HIGH)
                    time.sleep(0.3)
                    GPIO.output(red_pin, GPIO.LOW)
                    time.sleep(0.3)
                break

except KeyboardInterrupt:
    pass

finally:
    picam2.stop()
    GPIO.cleanup()
