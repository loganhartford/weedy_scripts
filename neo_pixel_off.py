from pi5neo import Pi5Neo

# Initialize the Pi5Neo class with 10 LEDs and an SPI speed of 800kHz
neo = Pi5Neo('/dev/spidev0.0', 10, 800)

# Fill the strip with a red color
b = 0
neo.fill_strip(int(255*b), int(255*b), int(255*b))
neo.update_strip()  # Commit changes to the LEDs