#!/usr/bin/python3
import os
from RPi import GPIO
from datetime import datetime
import time
from picamera2 import Picamera2

# Globals
BUTTON_PIN = 17
RED_LED_PIN = 27
GREEN_LED_PIN = 22
BLINK_DURATION = 0.3
CAPTURE_DIRECTORY = "/home/weedy/weedy_scripts/img"

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

def cleanup_gpio():
    GPIO.cleanup()

def blink_led(pin, times=3, duration=BLINK_DURATION):
    for _ in range(times):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(duration)

def initialize_camera():
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
    return picam2

def ensure_capture_directory():
    if not os.path.exists(CAPTURE_DIRECTORY):
        os.makedirs(CAPTURE_DIRECTORY)

def capture_image(picam2):
    try:
        filename = os.path.join(CAPTURE_DIRECTORY, f"captured_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        picam2.capture_file(filename)
        print(f"Image captured: {filename}")
        return 0
    except Exception as e:
        print(f"Error capturing image: {e}")
        return -1

def main():
    setup_gpio()
    ensure_capture_directory()
    picam2 = initialize_camera()

    try:
        blink_led(GREEN_LED_PIN)
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                result = capture_image(picam2)
                led_pin = GREEN_LED_PIN if result == 0 else RED_LED_PIN
                GPIO.output(led_pin, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(led_pin, GPIO.LOW)

                # Check if the button is still pressed after the status indication
                if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                    blink_led(RED_LED_PIN)
                    break

    except KeyboardInterrupt:
        pass
    finally:
        picam2.stop()
        cleanup_gpio()

if __name__ == "__main__":
    main()
