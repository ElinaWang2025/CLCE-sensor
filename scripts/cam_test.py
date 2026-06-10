import numpy as np
import cv2

import cv2

# 1. Initialize the webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Check if the webcam opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # 2. Capture frame-by-frame
    # ret is a boolean (True if frame grabbed successfully), frame is the actual image
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Failed to grab frame.")
        break

    # 3. Display the resulting frame in a window named 'Webcam Feed'
    cv2.imshow('Webcam Feed', frame)

    # 4. Break the loop if the 'q' key is pressed
    # waitKey(1) waits 1ms for a key event; ord('q') returns the ASCII value of 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Release the camera hardware and destroy all windows
cap.release()
cv2.destroyAllWindows()
