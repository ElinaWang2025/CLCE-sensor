import pickle
import gzip
import time
from picamera2 import Picamera2

import os
from gpiozero import LED, Button

# Define the LED on GPIO pin 17
led = LED(17)

cam = Picamera2()

still_config = cam.create_still_configuration(main={"size": (224, 224)})

video_config = cam.create_video_configuration(main={"size": (224, 224)}, controls={
    "AeEnable": False,  # Disable auto exposure
    "ExposureTime": 20000,  # Set exposure time to 20 ms (20000 microseconds)
    "AnalogueGain": 1.0,  # Set analogue gain to 1.0 (no gain)
    "AwbEnable": False,  # Disable auto white balance
})


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

cam.start()

button.wait_for_press()

print("Recording... press Ctrl+C to stop.")

button_is_pressed = False

log = {"frames": [], "timestamps": []}

try:
    while True:
        frame = cam.capture_array()
        log["frames"].append(frame)
        latest_frame_metadata = cam.capture_metadata()
        log["timestamps"].append(latest_frame_metadata['SensorTimestamp'])
    
        print(f"Timestamp: {log['timestamps'][-1]} ns",end="\r")


except KeyboardInterrupt:
    pass
print(len(log["frames"]), len(log["timestamps"]))
with gzip.open(f"{base_name}_log.pkl.gz", "wb") as f:
    pickle.dump(log, f)


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