import picamera2
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import os

cam = Picamera2()

still_config = cam.create_still_configuration(main={"size": (224, 224)})
video_config = cam.create_video_configuration(main={"size": (224, 224)})

# --- User inputs ---
sample_name = input("Enter sample name: ").strip().replace(" ", "_")
force_value = float(input("Enter force (N): "))
timestamp = int(time.time())
base_name = f"data/{sample_name}_{force_value:.3f}N_{timestamp}"

os.makedirs("data", exist_ok=True)

# --- Capture first image ---
cam.configure(still_config)
cam.start()
time.sleep(0.5)
cam.capture_file(f"{base_name}_start.jpg")
print(f"Captured start frame: {base_name}_start.jpg")
cam.stop()

# --- Record video ---
cam.configure(video_config)
encoder = H264Encoder(bitrate=4000000)
output = FfmpegOutput(f"{base_name}_video.mp4")

cam.start()
cam.start_encoder(encoder, output)
print("Recording... press Ctrl+C to stop.")

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

cam.stop_encoder()
print(f"Saved video: {base_name}_video.mp4")

# --- Capture final image ---
cam.stop()
cam.configure(still_config)
cam.start()
time.sleep(0.2)
cam.capture_file(f"{base_name}_end.jpg")
print(f"Captured end frame: {base_name}_end.jpg")
cam.stop()

print("Done.")