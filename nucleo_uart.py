import serial
import time

# Open the serial connection on /dev/ttyAMA0
ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)

def send_int(number):
    # Convert the integer to a string with newline and send it
    message = f"{number}\n"
    ser.write(message.encode())
    print(f"Sent: {message.strip()}")

def receive_int():
    input_buffer = []  # Buffer to store received characters

    while True:
        # Read one byte at a time
        received_char = ser.read(1).decode()  # Read one character and decode it

        if received_char in ('\n', '\r'):
            # End of input detected; convert to integer
            received_str = ''.join(input_buffer)  # Combine characters into a string
            try:
                received_int = int(received_str)  # Convert to integer
                print(f"Received Integer: {received_int}")
                return received_int
            except ValueError:
                print("Failed to convert received data to integer.")
                return None
        elif received_char:
            # Add the received character to the buffer if it's not the end of input
            input_buffer.append(received_char)

# Test the functions
try:
    # Send an integer
    # while True:
    #     send_int(12345)
    #     time.sleep(1)

    # Wait and receive an integer
    print("Waiting for integer...")
    received_value = receive_int()
    if received_value is not None:
        print(f"Loopback received value: {received_value}")

except KeyboardInterrupt:
    print("Test interrupted.")
finally:
    ser.close()
