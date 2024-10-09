from RPi import GPIO
from datetime import datetime
import time

GPIO.setmode(GPIO.BCM)
button_pin = 17
GPIO.setup(button_pin, GPIO.IN)


def capture_image():
    print("click")

try:
    print("Waiting for button press...")
    while True:
        if (GPIO.input(button_pin) == GPIO.HIGH):
            capture_image()
            time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()