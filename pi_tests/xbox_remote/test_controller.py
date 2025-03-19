import evdev

# Find the correct controller device
controller = None
for device_path in evdev.list_devices():
    device = evdev.InputDevice(device_path)
    if "8BitDo Ultimate 2C Wireless Controller" in device.name:
        controller = device
        print(f"Found controller: {device.name} at {device.path}")
        break

if not controller:
    print("Controller not found! Ensure it's connected.")
    exit(1)

# Read joystick and button events
print(f"Listening on {controller.path}... Move the joystick or press buttons.")

for event in controller.read_loop():
    if event.type == evdev.ecodes.EV_KEY:  # Button Presses
        print(f"Button {event.code} {'pressed' if event.value else 'released'}")
    elif event.type == evdev.ecodes.EV_ABS:  # Joystick Movement
        print(f"Joystick {event.code} moved to {event.value}")
