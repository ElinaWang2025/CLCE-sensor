import numpy as np
import cv2
print(cv2.getBuildInformation())

# Initialize the webcam (0 is usually the default built-in camera)
cap = cv2.VideoCapture(0)

# Check if the webcam opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Get capture properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0 or fps is None:
    fps = 30.0

# GStreamer udpsink settings (change host/port as needed)
host = "192.168.4.121"#"10.90.24.193"
port = 5000

# GStreamer pipeline: encode to H264 and send via RTP/UDP
gst_pipeline = (
"appsrc ! videoconvert ! x264enc threads=1 tune=zerolatency bitrate=800 speed-preset=ultrafast ! " \
"rtph264pay config-interval=1 pt=96 ! udpsink host={} port={} sync=false"
).format(host, port)

# OpenCV VideoWriter using GStreamer
out = cv2.VideoWriter(gst_pipeline, cv2.CAP_GSTREAMER, 0, fps, (width, height), True)
if not out.isOpened():
    print("Error: Could not open GStreamer pipeline for writing. Ensure OpenCV was built with GStreamer support.")
    cap.release()
    exit()

print(f"Streaming to {host}:{port} via GStreamer udpsink. Press Ctrl+C to stop.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break
        out.write(frame)
except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    cap.release()
    out.release()
    # cv2.destroyAllWindows()
