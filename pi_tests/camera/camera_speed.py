from picamera2 import Picamera2
from io import BytesIO
import time

def main():
    # Initialize the camera and configure for still images.
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
    picam2.configure(camera_config)
    picam2.start()

    num_images = 10
    start_time = time.perf_counter()

    for i in range(num_images):
        # Capture the image to an in-memory stream (not saved to disk)
        stream = BytesIO()
        picam2.capture_file(stream, format='jpeg')
        # If desired, you could reset or reuse the stream, but here we simply discard it.
    
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"Captured {num_images} images in {elapsed_time:.3f} seconds")
    print(f"Average time per image: {elapsed_time / num_images:.3f} seconds")

    picam2.close()

if __name__ == "__main__":
    main()
