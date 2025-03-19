from rpi_hardware_pwm import HardwarePWM
import time

pwm = HardwarePWM(pwm_channel=0, hz=20000, chip=2)
pwm.start(50)

pwm.change_duty_cycle(50)
pwm.change_frequency(20000)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()

