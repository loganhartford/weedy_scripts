import time
import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR
)
from adafruit_bno08x.i2c import BNO08X_I2C

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)

# Enable required sensor features
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

# Read and print sensor data
while True:
    time.sleep(0.5)
    
    # Accelerometer data
    accel_x, accel_y, accel_z = bno.acceleration
    print(f"Acceleration - X: {accel_x:.6f}, Y: {accel_y:.6f}, Z: {accel_z:.6f} m/s^2")

    # Gyroscope data
    gyro_x, gyro_y, gyro_z = bno.gyro
    print(f"Gyro - X: {gyro_x:.6f}, Y: {gyro_y:.6f}, Z: {gyro_z:.6f} rad/s")

    # Magnetometer data
    mag_x, mag_y, mag_z = bno.magnetic
    print(f"Magnetometer - X: {mag_x:.6f}, Y: {mag_y:.6f}, Z: {mag_z:.6f} uT")

    # Rotation vector (quaternion)
    quat_i, quat_j, quat_k, quat_real = bno.quaternion
    print(f"Rotation Quaternion - I: {quat_i:.6f}, J: {quat_j:.6f}, K: {quat_k:.6f}, Real: {quat_real:.6f}")

    print("-" * 50)
