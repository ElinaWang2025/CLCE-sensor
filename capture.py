import cv2
import subprocess
import time

# 1. Open the USB camera stream
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# 2. Force UNCOMPRESSED color format (YUYV/YUY2) for data integrity
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Force Auto Exposure OFF (1 = Manual Mode, 3 = Aperture Priority/Auto Mode)
subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=auto_exposure=1'])

# Drop the manual exposure time way down (e.g., to 50 or 100)
subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=exposure_time_absolute=50'])

# Lower the gain so the IR light doesn't cause sensor noise blowing out to white
subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=gain=10']) 


# 3. CRITICAL: Turn OFF Auto White Balance via V4L2 low-level Linux tools
# Hardware-level AWB will distort IR data if left on.
time.sleep(1) # Let the device node open first
subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=white_balance_automatic=0'])
# Optionally, lock temperature to a neutral mid-point (e.g., 4600)
subprocess.run(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl=white_balance_temperature=4600'])

print("Camera initialized. AWB disabled. Capturing full-spectrum frame...")
time.sleep(1) # Allow exposure to stabilize

ret, frame = cap.read()

if ret:
    # Frame will appear heavily pink/purple—this is the correct raw behavior 
    # of combined Visible + Near-Infrared light hitting the sensor arrays.
    cv2.imwrite("full_spectrum_capture.png", frame) # Save as PNG to avoid JPEG artifacts
    print("Success! Image saved as 'full_spectrum_capture.png'")
else:
    print("Error pulling frame.")

cap.release()
