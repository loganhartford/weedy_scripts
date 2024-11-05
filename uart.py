import serial
import time

# Open the serial connection on /dev/serial0
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

# Test data to send
test_message = "Hello, UART!\n"

try:
    while True:
        # Send the test message
        ser.write(test_message.encode())
        print(f"Sent: {test_message.strip()}")

        time.sleep(0.1)  # Small delay to allow data to be processed

        # Read the response
        response = ser.readline().decode().strip()
        print(f"Received: {response}")

        # Verify if the sent data matches the received data
        if response == test_message.strip():
            print("Loopback test successful!")
        else:
            print("Loopback test failed.")

        time.sleep(1)

except KeyboardInterrupt:
    print("Test interrupted.")
finally:
    ser.close()
