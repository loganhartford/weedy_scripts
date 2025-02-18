import numpy as np
import cv2
import math

pixel_points = np.array([
            [1543, 999], [1458, 54], [524, 1012], [552, 59]
                                                ], dtype=np.float32)
ground_points = np.array([
    [20, 10], [240, 10], [20, 245], [240, 245]
                                        ], dtype=np.float32)
H, _ = cv2.findHomography(pixel_points, ground_points)

def homography_transform( pixel):
    image_point = np.array([pixel[0], pixel[1], 1], dtype=np.float32)
    ground_point = np.dot(H, image_point)
    ground_point /= ground_point[2]

    return ground_point[:2]
