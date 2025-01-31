from PIL import Image as PILImage
from io import BytesIO
import numpy as np
import requests
import cv2


def get_img():
        response = requests.get("http://localhost:8000")
        response.raise_for_status()

        image = PILImage.open(BytesIO(response.content))
        image_np = np.array(image)[:, :, ::-1]

        print("Image fetched from camera")

        return image_np
    
def capture_and_save_image(filename="./captured_image.jpg"):
    img = get_img()

    cv2.imwrite(filename, img)

if __name__ == "__main__":
    get_img()