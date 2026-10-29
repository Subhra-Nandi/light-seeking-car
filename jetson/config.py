# ============================================================
# config.py
# All tunable values in one place
# Change HSV ranges here after real-world calibration
# ============================================================

import numpy as np

# --- Serial Port ---
# Change this to match your system
# Linux (Jetson): usually "/dev/ttyUSB0" or "/dev/ttyACM0"
SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE   = 9600

# --- Camera ---
CAMERA_INDEX  = 0       # 0 = first camera (CSI or USB)
FRAME_WIDTH   = 640
FRAME_HEIGHT  = 480
FRAME_FPS     = 30

# --- HSV Colour Ranges ---
# Format: [lower_bound, upper_bound] as numpy arrays [H, S, V]
# Hue range in OpenCV: 0-179
# Saturation & Value: 0-255

COLOUR_RANGES = {
    "RED": [
        # Red wraps around in HSV — needs two ranges
        (np.array([0,   120, 70]),  np.array([10,  255, 255])),
        (np.array([170, 120, 70]),  np.array([179, 255, 255])),
    ],
    "GREEN": [
        (np.array([35, 80, 50]),   np.array([85,  255, 255])),
    ],
    "BLUE": [
        (np.array([100, 80, 50]),  np.array([130, 255, 255])),
    ],
    "YELLOW": [
        (np.array([20, 100, 100]), np.array([35,  255, 255])),
    ],
}

# --- Detection Sensitivity ---
# Minimum number of pixels to confirm a colour detection
MIN_PIXEL_COUNT = 1000
