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
    # Open the serial connection for reading
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=1)
    
    try:
        while True:
            if ser.in_waiting >= 5:
                data = ser.read(5)
                try:
                    message_type, axis, position = parse_message(data)
                    print(f"Received: Message Type {message_type}, Axis {axis}, Position {position}, Message {list(data)}")
                    
                    if message_type == 0x02:  # Data message from Nucleo
                        # Process data as needed
                        print(f"Processing data: Axis {axis}, Position {position}")
                        
                        # Send acknowledgment
                        ack_message = construct_message(0x03, axis, position)
                        ser.write(ack_message)
                        print(f"Sent ACK: {list(ack_message)}")
                    elif message_type == 0x01:
                        # Should not receive command messages here, but handle just in case
                        print("Unexpected command message received.")
                    else:
                        # Do not acknowledge acknowledgments or errors to prevent ack loops
                        pass
                    
                except ValueError as e:
                    print(f"Error parsing message: {e}")
                    # Send error message back
                    error_message = construct_message(0x04, 0, 0)
                    ser.write(error_message)
                    print(f"Sent Error: {list(error_message)}")
    
            time.sleep(0.1)  # Short delay to prevent high CPU usage
    
    except KeyboardInterrupt:
        print("Read script interrupted by user.")
    
    finally:
        ser.close()

if __name__ == "__main__":
    main()
