import cv2
import numpy as np
import os

# -------------------------------------------------------------------------
# 1. LOCK USB CAMERA HARDWARE CONTROLS VIA V4L2
# -------------------------------------------------------------------------
CAM_INDEX = 0  # Adjust if needed (/dev/video0)

# Disable Auto-Exposure (1 = Manual Mode in V4L2) and set a fixed exposure
os.system(f"v4l2-ctl -d /dev/video{CAM_INDEX} -c auto_exposure=1")
os.system(f"v4l2-ctl -d /dev/video{CAM_INDEX} -c exposure_time_absolute=150")

# Disable Auto-White Balance (AWB) and lock Gain
os.system(f"v4l2-ctl -d /dev/video{CAM_INDEX} -c white_balance_automatic=0")
os.system(f"v4l2-ctl -d /dev/video{CAM_INDEX} -c gain=0")

# -------------------------------------------------------------------------
# 2. OPEN CV USB CAPTURE SETUP
# -------------------------------------------------------------------------
cap = cv2.VideoCapture(CAM_INDEX)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

center_point = None

def mouse_callback(event, x, y, flags, param):
    global center_point
    if event == cv2.EVENT_LBUTTONDOWN:
        # Ignore accidental clicks too close to frame boundaries
        if y < 15 or y > 705 or x < 15 or x > 1265:
            print(f"Ignored edge click at ({x}, {y}). Please click inside the active CLCE region.")
            return
        center_point = (int(x), int(y))
        print(f"ROI Center set to: ({center_point}, {center_point[1]})")

cv2.namedWindow("USB NoIR CLCE Tracker")
cv2.setMouseCallback("USB NoIR CLCE Tracker", mouse_callback)

print("--- USB NoIR CLCE Wavelength Shift Tracker ---")
print("Click on the center of the active CLCE deformation area.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame from USB camera.")
        break

    display_frame = frame.copy()

    if center_point is not None:
        cx, cy = center_point

        # Explicitly define fixed positive integer radii (in pixels)
        radii = [2-6]
        
        # OpenCV BGR: Channel 2 = Red (near-IR crosstalk sensitivity)
        red_channel = frame[:, :, 2]
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ring_red_means = []
        ring_gray_means = []

        for r in radii:
            r_int = int(r)
            if r_int <= 0:
                continue  # Guard against non-positive radius values

            mask = np.zeros(gray_frame.shape, dtype=np.uint8)
            cv2.circle(mask, (cx, cy), r_int, 255, thickness=2)

            # Calculate mean only if mask contains valid pixels
            if cv2.countNonZero(mask) > 0:
                mean_red = cv2.mean(red_channel, mask=mask)
                mean_gray = cv2.mean(gray_frame, mask=mask)

                ring_red_means.append(mean_red)
                ring_gray_means.append(mean_gray)

                # Draw rings on output overlay
                cv2.circle(display_frame, (cx, cy), r_int, (0, 255, 0), 1)

        if ring_red_means:
            avg_red_intensity = np.mean(ring_red_means)
            avg_gray_intensity = np.mean(ring_gray_means)

            # Draw center marker and metrics
            cv2.circle(display_frame, (cx, cy), 3, (0, 0, 255), -1)
            cv2.putText(display_frame, f"NIR Red Channel Intensity: {avg_red_intensity:.1f}", 
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(display_frame, f"Grayscale Broadband Intensity: {avg_gray_intensity:.1f}", 
                        (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("USB NoIR CLCE Tracker", display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()