import cv2
import time
import subprocess

# 1. Open the camera using the standard Video4Linux backend
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# 2. Force uncompressed YUYV format to retain the full spectrum color pixels
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

time.sleep(1) # Let the camera stream initialize

# 3. CRITICAL: Turn OFF Auto-Exposure using OpenCV's built-in hooks
# 1 = Manual Mode, 3 = Auto Mode (This translates cleanly to most USB chips)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 

# 4. Drastically drop the manual exposure value down to stop the whiteout
# Standard OpenCV range is typically 0 to 10000 or -1 to -13. 
# Try a small absolute value like 20 to heavily dim the sensor.
cap.set(cv2.CAP_PROP_EXPOSURE, 10)

# 5. Drop the gain/brightness amplification so the IR LEDs don't clip pixels to white
cap.set(cv2.CAP_PROP_GAIN, 5)


# # Force Auto Exposure OFF (1 = Manual Mode, 3 = Aperture Priority/Auto Mode)
# subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=auto_exposure=1'])

# # Drop the manual exposure time way down (e.g., to 50 or 100)
# subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=exposure_time_absolute=50'])

# # Lower the gain so the IR light doesn't cause sensor noise blowing out to white
# subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=gain=10']) 


print("Capturing frame with forced low exposure...")
time.sleep(1) # Allow sensor gain adjustments to settle

ret, frame = cap.read()
if ret:
    cv2.imwrite("dimmed_spectrum_capture.png", frame)
    print("Success! Saved as 'dimmed_spectrum_capture.png'")
else:
    print("Failed to pull frame.")

cap.release()
