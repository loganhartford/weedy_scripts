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
    # Open the serial connection
    ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, timeout=0.1)
    
    try:
        while True:
            # Step 1: Send Command
            axis = 1
            position = 423  # You can change this value as needed
            message = construct_message(0x01, axis, position)  # Message Type 0x01 for Command
            ser.write(message)
            print(f"Sent Command: Axis {axis}, Position {position}, Message {list(message)}")
            
            # Step 2: Wait for Acknowledgment
            ack_received = False
            ack_timeout = 5  # seconds
            ack_start_time = time.time()
            buffer = bytearray()
            
            while not ack_received and (time.time() - ack_start_time) < ack_timeout:
                data = ser.read(ser.in_waiting or 1)
                if data:
                    buffer.extend(data)
                    # Try to parse complete messages
                    while len(buffer) >= 5:
                        message = buffer[:5]
                        try:
                            message_type, resp_axis, resp_position = parse_message(message)
                            if message_type == 0x03:  # Acknowledgment
                                print(f"Received ACK: Axis {resp_axis}, Position {resp_position}")
                                ack_received = True
                                break
                            elif message_type == 0x04:  # Error
                                print(f"Received Error: Axis {resp_axis}, Position {resp_position}")
                                print("Resending Command...")
                                ser.write(message)
                                ack_start_time = time.time()  # Reset timeout
                                buffer = buffer[5:]  # Remove processed message
                                break
                            else:
                                print(f"Received unexpected message type: {message_type}")
                                buffer = buffer[5:]  # Remove processed message
                        except ValueError as e:
                            print(f"Error parsing message: {e}")
                            buffer = buffer[1:]  # Remove one byte and retry
                else:
                    time.sleep(0.1)
            
            if not ack_received:
                print("Timeout waiting for acknowledgment. Resending Command...")
                continue  # Go back to the start of the loop to resend the command
            
            # Step 3: Check for Incoming Data
            data_check_duration = 1  # seconds
            data_check_start_time = time.time()
            buffer = bytearray()
            
            while (time.time() - data_check_start_time) < data_check_duration:
                data = ser.read(ser.in_waiting or 1)
                if data:
                    buffer.extend(data)
                    # Try to parse complete messages
                    while len(buffer) >= 5:
                        message = buffer[:5]
                        try:
                            message_type, axis, position = parse_message(message)
                            print(f"Received: Message Type {message_type}, Axis {axis}, Position {position}, Message {list(message)}")
                            
                            if message_type == 0x02:  # Data message
                                # Process data as needed
                                print(f"Processing data: Axis {axis}, Position {position}")
                                
                                # Send acknowledgment
                                ack_message = construct_message(0x03, axis, position)
                                ser.write(ack_message)
                                print(f"Sent ACK: {list(ack_message)}")
                            else:
                                print(f"Received unexpected message type: {message_type}")
                            
                            buffer = buffer[5:]  # Remove processed message
                        except ValueError as e:
                            print(f"Error parsing message: {e}")
                            buffer = buffer[1:]  # Remove one byte and retry
                else:
                    time.sleep(0.1)
            
            # Step 4: Wait before sending the next command
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
