import qrcode
import os

data_list = ["qr_1", "qr_2", "qr_3"]  # List of strings to generate QR codes for
output_dir = "qr_codes"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

for data in data_list:
    img = qrcode.make(data)
    img.save(os.path.join(output_dir, f"{data}.png"))