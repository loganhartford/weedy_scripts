from RPi import GPIO
# from picamera2 import Picamera2
from datetime import datetime
import time

# camera = Picamera2()

GPIO.setmode(GPIO.BCM)
button_pin = 17
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# camera.start()

def capture_image():
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # file_name = f"/home/pi/weeds/image_{timestamp}.jpg"
    # camera.capture_file(file_name)
    # print(f"Image captured: {file_name}")
    print("click")

try:
    print("Waiting for button press...")
    while True:
        if GPIO.input(button_pin) == GPIO.LOW:
            capture_image()
            time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()