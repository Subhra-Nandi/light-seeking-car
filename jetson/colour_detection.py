# ============================================================
# colour_detection.py
# Captures camera frames, converts to HSV,
# detects colour and returns colour name as string
# ============================================================

import cv2
import numpy as np
from config import COLOUR_RANGES, MIN_PIXEL_COUNT, CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, FRAME_FPS


class ColourDetector:

    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS,          FRAME_FPS)

        if not self.cap.isOpened():
            raise RuntimeError("Camera could not be opened. Check CAMERA_INDEX in config.py")

        print("Camera initialized.")

    def detect(self):
        """
        Captures one frame and returns the detected colour name.
        Returns: "RED", "GREEN", "BLUE", "YELLOW", or "NONE"
        """
        ret, frame = self.cap.read()
        if not ret:
            print("Warning: Failed to read frame.")
            return "NONE"

        # Focus on center region only — ignore edges
        h, w, _ = frame.shape
        roi = frame[h//4 : 3*h//4, w//4 : 3*w//4]

        # Convert BGR → HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        detected_colour = "NONE"
        max_pixels      = MIN_PIXEL_COUNT  # Must exceed this to count

        for colour_name, ranges in COLOUR_RANGES.items():
            mask = None

            for (lower, upper) in ranges:
                partial_mask = cv2.inRange(hsv, lower, upper)
                mask = partial_mask if mask is None else cv2.bitwise_or(mask, partial_mask)

            pixel_count = cv2.countNonZero(mask)

            if pixel_count > max_pixels:
                max_pixels      = pixel_count
                detected_colour = colour_name

        return detected_colour

    def get_frame(self):
        """Returns raw frame — useful for debugging/display."""
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Camera released.")
