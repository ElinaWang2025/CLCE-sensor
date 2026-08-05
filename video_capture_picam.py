import subprocess
import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput
import os
from gpiozero import LED, Button

# Define the LED on GPIO pin 17
led = LED(17)

cam = Picamera2()

still_config = cam.create_still_configuration(main={"size": (224, 224)})
TARGET_FPS = 32.0
video_config = cam.create_video_configuration(controls={
    'FrameRate': TARGET_FPS,
    "FrameDurationLimits": (33333, 33333), # Forces exactly 33.3ms per frame (30 FPS)
    "ExposureTime": 30000,                  # Keeps exposure under 33ms limit
    "AnalogueGain": 2.0                     # Boost brightness digitally instead of slowing down FPS
    }, main={"size": (224, 224)})
# cam.configure(video_config)

# --- User inputs ---
sample_name = input("Enter sample name: ").strip().replace(" ", "_")
force_value = float(input("Enter force (N): "))
timestamp = int(time.time())
base_name = f"data/{sample_name}_{force_value:.3f}N_{timestamp}"
h264_temp_file = f"{base_name}_temp.h264"
mp4_final_file = f"{base_name}_video.mp4"

os.makedirs("data", exist_ok=True)

button = Button(4)  # GPIO 4, pin 7 

# --- Capture first image ---
led.on()     # Turn LED on
cam.configure(still_config)
cam.start()
time.sleep(0.5)
cam.capture_file(f"{base_name}_start.jpg")
print(f"Captured start frame: {base_name}_start.jpg")
cam.stop()

# --- Record video ---
cam.configure(video_config)
encoder = H264Encoder(bitrate=4000000)
# output = FfmpegOutput(f"{base_name}_video.mp4")

cam.start()

# button.wait_for_press()

# cam.start_encoder(encoder, output)
cam.start_recording(encoder, h264_temp_file, quality=Quality.HIGH)
# 3. Fetch the metadata from the absolute first frame to find its hardware timestamp
first_frame_metadata = cam.capture_metadata()
camera_start_timestamp = first_frame_metadata['SensorTimestamp'] # In nanoseconds

print(f"Sync Anchored! Camera start ns: {camera_start_timestamp}")
print("Recording... press Ctrl+C to stop.")

button_is_pressed = False

try:
    while True:
        latest_frame_metadata = cam.capture_metadata()
        camera_latest_timestamp = latest_frame_metadata['SensorTimestamp'] # In nanoseconds
        # Calculate how many seconds passed since the camera stream started
        elapsed_nanoseconds = camera_latest_timestamp - camera_start_timestamp

        # 4. Convert nanoseconds to fractional video seconds (e.g., 1.452 seconds)
        video_relative_seconds = elapsed_nanoseconds / 1_000_000_000.0
        print(f"Video relative timestamp: {video_relative_seconds:.4f}s", end="\r")

        if button.is_pressed and not button_is_pressed:
            button_is_pressed = True
            print(f"Trigger timestamp: {video_relative_seconds:.4f}s")
        time.sleep(0.01)
except KeyboardInterrupt:
    pass

# cam.stop_encoder()
cam.stop_recording()
# print(f"Saved video: {base_name}_video.mp4")
ffmpeg_cmd = [
    "ffmpeg", "-y", 
    "-r", str(TARGET_FPS), 
    "-i", h264_temp_file, 
    "-c", "copy", 
    mp4_final_file
]
subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print(f"Video saved perfectly at {TARGET_FPS} FPS: {mp4_final_file}")

# --- Capture final image ---
cam.stop()
cam.configure(still_config)
cam.start()
time.sleep(0.2)
cam.capture_file(f"{base_name}_end.jpg")
print(f"Captured end frame: {base_name}_end.jpg")
cam.stop()
led.off()    # Turn LED off

print("Done.")