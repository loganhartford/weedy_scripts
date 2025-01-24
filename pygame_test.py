import pygame
import time

# Initialize pygame
pygame.init()

# Initialize joystick
if pygame.joystick.get_count() == 0:
    print("No joystick detected. Ensure it's connected.")
    exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Found joystick: {joystick.get_name()}")
print("Move the left joystick to simulate velocity outputs.")

# Speed scaling factors
SPEED_SCALE = 0.5  # Adjust max forward/backward speed
TURN_SCALE = 1.0   # Adjust max turning speed

# Main loop to read joystick and simulate Twist-like output
running = True
while running:
    pygame.event.pump()  # Process event queue

    # Left joystick: Axis 0 (X for turning), Axis 1 (Y for forward/backward)
    linear_x = -joystick.get_axis(1) * SPEED_SCALE  # Forward/Backward (inverted Y-axis)
    angular_z = joystick.get_axis(0) * TURN_SCALE   # Left/Right

    print(f"Simulated Output -> Linear: {linear_x:.2f}, Angular: {angular_z:.2f}")

    # Exit if button 0 (A button on many controllers) is pressed
    if joystick.get_button(0):
        print("Exiting...")
        running = False

    time.sleep(0.1)  # 10Hz update rate

# Quit pygame
pygame.quit()
