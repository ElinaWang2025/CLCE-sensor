import cv2

# Open the USB camera (0 is usually the built-in or first USB webcam)
cap = cv2.VideoCapture(0)

# FORCE the USB camera to output a standard compressed color format (MJPEG)
# This forces the camera firmware to transmit full-color channels
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Optional: Set your desired resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Software fallback: if the driver passes a 1-channel grayscale matrix, 
    # force convert it to a 3-channel BGR matrix so your pipeline stays color-compliant
    if len(frame.shape) == 2 or frame.shape[2] == 1:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    cv2.imshow("USB Camera - Forced RGB Mode", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
