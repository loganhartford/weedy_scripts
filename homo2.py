import cv2
import numpy as np

# Example: more than 4 corresponding points between the image (pixel) and ground (robot) frames.
# Ensure these are collected such that they cover the area of interest.
pixel_points = np.array([
    [1417, 1066],
    [1004, 1072],
    [586, 1079],
    [1284, 934],
    [720, 943], 
    [1002, 861],
    [1403, 650],
    [1202, 652],
    [1000, 654],
    [795, 656],
    [591, 659],
    [996, 452],
    [1268, 377],
    [720, 380],
    [1389, 252],
    [993, 253],
    [591, 256],
], dtype=np.float32)

x = 0
y = 55
ground_points = np.array([
    [x-30, y-30],
    [x-30, y+65],
    [x-30, y+160],
    [x, y],
    [x, y+130],
    [x+17.5, y+65],
    [x+65, y-30],
    [x+65, y+17.5],
    [x+65, y+65],
    [x+65, y+112.5],
    [x+65, y+160],
    [x+112.5, y+65],
    [x+130, y],
    [x+130, y+130],
    [x+160, y-30],
    [x+160, y+65],
    [x+160, y+160],
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
    # [1417, 1066],
    [1004, 1072],
    # [586, 1079],
    # [1284, 934],
    # [720, 943], 
    # [1002, 861],
    # [1403, 650],
    # [1202, 652],
    # [1000, 654],
    # [795, 656],
    # [591, 659],
    # [996, 452],
    # [1268, 377],
    # [720, 380],
    [1389, 252],
    # [993, 253],
    # [591, 256],
], dtype=np.float32)

test_ground_points = np.array([
    # [x-30, y-30],
    [x-30, y+65],
    # [x-30, y+160],
    # [x, y],
    # [x, y+130],
    # [x+17.5, y+65],
    # [x+65, y-30],
    # [x+65, y+17.5],
    # [x+65, y+65],
    # [x+65, y+112.5],
    # [x+65, y+160],
    # [x+112.5, y+65],
    # [x+130, y],
    # [x+130, y+130],
    [x+160, y-30],
    # [x+160, y+65],
    # [x+160, y+160],
], dtype=np.float32)

for i, point in enumerate(test_pixel_points):
    transformed_point = homography_transform(point, H)
    print(f"Error: {np.linalg.norm(transformed_point - test_ground_points[i])} mm")