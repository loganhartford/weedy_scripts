import cv2
import numpy as np

# Example: more than 4 corresponding points between the image (pixel) and ground (robot) frames.
# Ensure these are collected such that they cover the area of interest.
pixel_points = np.array([
    [1291, 953],
    [694, 964],
    [1410, 652],
    [986, 659],
    [563, 668],
    [1385, 242],
    [977, 251],
    [571, 258],
    [982, 451],
    # [991, 876],
    # [1198, 655],
    # [774, 664],
    # [1262, 371],
    # [699, 382],
], dtype=np.float32)

x = 0
y = 30
ground_points = np.array([
    [x+30, y+30],
    [x+30, y+160],
    [x+95, y+0],
    [x+95, y+95],
    [x+95, y+190],
    [x+190, y+0],
    [x+190, y+95],
    [x+190, y+190],
    [y+95, x+142.5]
    # [x+47.5, y+95],
    # [x+95, y+47.5],
    # [x+95, y+142.5],
    # [x+160, y+30],
    # [x+160, y+160],
], dtype=np.float32)

# Compute the homography using RANSAC.
H, status = cv2.findHomography(pixel_points, ground_points, cv2.RANSAC, 5.0)

if H is not None:
    print("Computed Homography:\n", H)
    print("Inlier status for each point:\n", status.ravel())
else:
    print("Homography computation failed.")

# Function to transform a pixel point using the computed homography.
def homography_transform(pixel, H):
    # Convert the point to homogeneous coordinates.
    image_point = np.array([pixel[0], pixel[1], 1], dtype=np.float32)
    # Apply the homography matrix.
    ground_point = np.dot(H, image_point)
    # Normalize to convert from homogeneous coordinates.
    ground_point /= ground_point[2]
    return ground_point[:2]

# Test
test_pixel_points = np.array([
    [991, 876],
    [1198, 655],
    [774, 664],
    [1262, 371],
    [699, 382],
], dtype=np.float32)

test_ground_points = np.array([
    [x+47.5, y+95],
    [x+95, y+47.5],
    [x+95, y+142.5],
    [x+160, y+30],
    [x+160, y+160],
], dtype=np.float32)

for i, point in enumerate(test_pixel_points):
    transformed_point = homography_transform(point, H)
    print(f"Error: {np.linalg.norm(transformed_point - test_ground_points[i])} mm")