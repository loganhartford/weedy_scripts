import cv2
import numpy as np

# Select points with get_pixel.py
# Select from bottom right to top left, moving all the way across one level before proceeding to the next
pixel_points = np.array([
    # [1417, 1066],
    # [1004, 1072],
    # [586, 1079],
    [1268, 952], 
    [615, 958], 
    [943, 859], 
    [1403, 610], 
    [1173, 610], 
    [941, 611], 
    [707, 612], 
    [472, 613], 
    [939, 369], 
    [1253, 279], 
    [621, 279], 
    [1390, 133], 
    [937, 133], 
    [477, 130]
], dtype=np.float32)

x = 0
y = 44.81
ground_points = np.array([
    # [x-35.7, y-33.99],
    # [x-35.7, y+75.51],
    # [x-35.7, y+185.01],
    [x, y],
    [x, y+151.02],
    [x+21.8, y+75.51],
    [x+79.3, y-33.99],
    [x+79.3, y+20.76],
    [x+79.3, y+75.51],
    [x+79.3, y+130.26],
    [x+79.3, y+185.01],
    [x+136.8, y+75.51],
    [x+158.6, y],
    [x+158.6, y+151.02],
    [x+194.3, y-33.99],
    [x+194.3, y+75.51],
    [x+194.3, y+185.01],
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