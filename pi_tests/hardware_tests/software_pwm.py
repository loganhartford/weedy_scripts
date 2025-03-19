import lgpio
import time

PWM_PIN = 12

print("PWM test")
chip = lgpio.gpiochip_open(2)
lgpio.tx_pwm(chip, PWM_PIN, 20000, 50000)

try:
    while True:
        time.sleep(1)

finally:
    lgpio.gpiochip_close(chip)

