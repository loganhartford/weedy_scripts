import serial
import time

# Open the serial connection on /dev/serial0
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

# Data to send
axis = 1
byte1 = 4
byte2 = 2
byte3 = 3
checksum = (axis + byte1 + byte2 + byte3) % 256
data = bytes([axis, byte1, byte2, byte3, checksum])

try:
    while True:
        ser.write(data)
        print(f"Sent: {list(data)}")

        time.sleep(0.1)

        response = ser.read(6)
        print(f"Received: {list(response)}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Test interrupted.")
finally:
    ser.close()
