import serial
import time

def construct_message(message_type, axis, position):
    # Ensure message_type is valid
    if message_type not in [0x01, 0x02, 0x03, 0x04]:
        raise ValueError("Invalid message type.")
    
    # Ensure axis is within valid range
    if axis not in [0, 1, 2]:
        raise ValueError("Axis must be 0, 1, or 2.")
    
    # Ensure position is within valid range (0-999)
    if not (0 <= position <= 999):
        raise ValueError("Position must be between 0 and 999.")
    
    # Split position into high and low bytes
    pos_high = (position >> 8) & 0xFF
    pos_low = position & 0xFF
    
    # Compute checksum
    checksum = (message_type + axis + pos_high + pos_low) % 256
    
    # Construct message
    message = bytes([message_type, axis, pos_high, pos_low, checksum])
    
    return message

def parse_message(message):
    # Message should be 5 bytes
    if len(message) != 5:
        raise ValueError("Message must be 5 bytes long.")
    
    message_type = message[0]
    axis = message[1]
    pos_high = message[2]
    pos_low = message[3]
    checksum = message[4]
    
    # Recompute checksum
    calculated_checksum = (message_type + axis + pos_high + pos_low) % 256
    
    if checksum != calculated_checksum:
        raise ValueError("Checksum does not match.")
    
    # Reconstruct position
    position = (pos_high << 8) | pos_low
    
    return message_type, axis, position

def main():
    # Open the serial connection for writing
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
    
    try:
        while True:
            # Example data to send
            axis = 1
            position = 423  # You can change this value as needed
            
            # Construct and send the command message
            message = construct_message(0x01, axis, position)  # Message Type 0x01 for Command
            ser.write(message)
            print(f"Sent Command: Axis {axis}, Position {position}, Message {list(message)}")
            
            # Wait for acknowledgment or error
            start_time = time.time()
            while True:
                if ser.in_waiting >= 5:
                    response = ser.read(5)
                    try:
                        resp_type, resp_axis, resp_position = parse_message(response)
                        if resp_type == 0x03:  # Acknowledgment
                            print(f"Received ACK: Axis {resp_axis}, Position {resp_position}")
                            break
                        elif resp_type == 0x04:  # Error
                            print(f"Received Error: Axis {resp_axis}, Position {resp_position}")
                            print("Resending Command...")
                            ser.write(message)
                            start_time = time.time()  # Reset timeout
                        else:
                            print(f"Received unexpected message type: {resp_type}")
                    except ValueError as e:
                        print(f"Error parsing response: {e}")
                elif time.time() - start_time > 5:
                    print("Timeout waiting for acknowledgment.")
                    print("Resending Command...")
                    ser.write(message)
                    start_time = time.time()
                time.sleep(0.1)
            
            time.sleep(1)  # Wait before sending the next command
    
    except KeyboardInterrupt:
        print("Write script interrupted by user.")
    
    finally:
        ser.close()

if __name__ == "__main__":
    main()
