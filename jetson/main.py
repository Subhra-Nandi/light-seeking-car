# ============================================================
# main.py
# Entry point for Jetson Nano
# Ties colour detection + serial communication together
# Run this file to start the car: python3 main.py
# ============================================================

import time
from colour_detection import ColourDetector
from serial_comm      import SerialComm


def main():
    print("Starting Light Seeking & Colour Detection Car...")

    # Initialize camera and serial
    detector = ColourDetector()
    comm     = SerialComm()

    last_command = ""

    try:
        while True:

            # Step 1 — Detect colour from camera
            colour = detector.detect()

            # Step 2 — Only send if command changed (avoid flooding serial)
            if colour != last_command:
                comm.send_command(colour)
                print(f"Colour detected: {colour} → Command sent: {colour}")
                last_command = colour

            # Step 3 — Read any response from Arduino (optional debug)
            response = comm.read_response()
            if response:
                print(f"Arduino says: {response}")

            # Step 4 — Small delay to keep loop stable
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping car...")
        comm.send_command("RED")   # Send stop command before exit
        time.sleep(0.5)

    finally:
        detector.release()
        comm.close()
        print("Shutdown complete.")


if __name__ == "__main__":
    main()
