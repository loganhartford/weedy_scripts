import cv2
import numpy as np

# Select points with get_pixel.py
# Select from bottom right to top left, moving all the way across one level before proceeding to the next
pixel_points = np.array([
    [1401, 1053], 
    [929, 1055], 
    [451, 1058], 
    [1302, 949], 
    [555, 951], 
    [1253, 897], 
    [604, 900], 
    [929, 804], 
    [1388, 559], 
    [1160, 558], 
    [928, 558], 
    [696, 558], 
    [463, 559], 
    [927, 317], 
    [1241, 229], 
    [611, 227], 
    [1379, 84], 
    [927, 82], 
    [469, 79]], dtype=np.float32)

x = 0
y = 23
ground_points = np.array([
    [x-24.47, y-23.3],
    [x-24.47, y+86.2],
    [x-24.47, y+195.7],
    [x, y],
    [x, y+172.39],
    [x+11.23, y+10.69],
    [x+11.23, y+161.71],
    [x+33.03, y+86.2],
    [x+90.53, y-23.3],
    [x+90.53, y+31.45],
    [x+90.53, y+86.2],
    [x+90.53, y+140.95],
    [x+90.53, y+195.7],
    [x+148.03, y+86.2],
    [x+169.83, y+10.69],
    [x+169.83, y+161.71],
    [x+205.53, y-23.3],
    [x+205.53, y+86.2],
    [x+205.53, y+195.7],
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
pred = [
    (899, 579),
    (877, 363),
    (1035, 574),
    (866, 342),
    (1294, 389),
]

actual = [
    (899, 584),
    (861, 382),
    (998, 593),
    (863, 363),
    (1299, 401),
]

for i, point in enumerate(pred):
    pred_mm = homography_transform(point, H).round(2)
    actual_mm = homography_transform(actual[i], H).round(2)
    euclidean_distance = np.linalg.norm(pred_mm - actual_mm)
    print(f"Predicted: {pred_mm}, Actual: {actual_mm}, Euclidean Distance: {euclidean_distance:.2f}")