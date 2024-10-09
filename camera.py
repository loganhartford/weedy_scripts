#!/usr/bin/python3
from RPi import GPIO
from datetime import datetime
import time
import random

def random_sign():
    return random.choice([0, -1])

GPIO.setmode(GPIO.BCM)

button_pin = 17
red_pin = 27
green_pin = 22
GPIO.setup(button_pin, GPIO.IN)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)


def capture_image():
    ret = random_sign()
    if ret:
        print("error")
        return ret
    print("click")
    return ret

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
    GPIO.cleanup()