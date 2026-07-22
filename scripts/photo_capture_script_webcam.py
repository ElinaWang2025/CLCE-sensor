# On the Pi — simple capture script
# Step 1: Data Collection on the Pi
# Capture images with consistent framing — same distance, lighting, angle every time. 
# Label each image with the known force value at capture time (e.g. from a reference load cell).

# import picamera2, time
import time
import os
import cv2

# cam = picamera2.Picamera2()
# cam.configure(cam.create_still_configuration(main={"size": (224, 224)}))
# cam.start()

# Initialize the webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Check if the webcam opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit(1)

# Get capture properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0 or fps is None:
    fps = 30.0

def get_force_value(prompt="Enter force (N): "):
    while True:
        try:
            user_input = input(prompt)
        except EOFError:
            print("No input received; using force = 0.0 N")
            return 0.0
        if user_input is None:
            print("No input; using force = 0.0 N")
            return 0.0
        s = user_input.strip()
        if s == "":
            print("Empty input; using force = 0.0 N")
            return 0.0
        try:
            return float(s)
        except ValueError:
            print("Invalid number; please enter a numeric value (e.g. 12.3).")


# ensure output directory exists
os.makedirs("data", exist_ok=True)

force_value = get_force_value()
timestamp = int(time.time())
ret, frame = cap.read()
if not ret or frame is None:
    print("Error: Failed to read frame from webcam.")
    cap.release()
    exit(1)

cv2.imwrite(f"data/{force_value:.3f}_{timestamp}.jpg", frame)
print(f"Saved image to data/{force_value:.3f}_{timestamp}.jpg")
cap.release()