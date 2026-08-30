import pickle
import gzip
import time
from picamera2 import Picamera2
from signal import pause

import os
from gpiozero import LED, Button

# Define the LED on GPIO pin 18
led = LED(18)

cam = Picamera2()

still_config = cam.create_still_configuration(main={"size": (1024, 1024)})

video_config = cam.create_video_configuration(main={"size": (1024, 1024)}, controls={
    "AeEnable": False,  # Disable auto exposure
    "ExposureTime": 12000,  # Set exposure time to 12 ms
    "AnalogueGain": 4.0,  # Set analogue gain to 4.0
    "AwbEnable": False,  # Disable auto white balance
    "FrameRate": 40,  # Set framerate to 40 fps
})


# --- User inputs ---
sample_name = input("Enter sample name: ").strip().replace(" ", "_")
force_value = float(input("Enter force (N): "))
timestamp = int(time.time())
base_name = f"data/{sample_name}_{force_value:.3f}N_{timestamp}"
h264_temp_file = f"{base_name}_video.mp4"

os.makedirs("data", exist_ok=True)

# trigger on GPIO 4 (pin 7) for voltage trigger
button = Button(4,pull_up=False)  # GPIO 4, pin 7 (may need to toggle pull_up to False if you want to use an external pull-down resistor)
# trigger_pin = Button(4, pull_up=True)

# --- Capture first image ---
led.on()     # Turn LED on
cam.configure(still_config)
cam.start()
time.sleep(0.5)

cam.capture_file(f"{base_name}_start.jpg")
print(f"Captured start frame: {base_name}_start.jpg")
cam.stop()
time.sleep(1)
led.off() 
# --- Record video ---
cam.configure(video_config)

cam.start()

button.wait_for_press()
t_trigger = time.time()
led.on() 
time.sleep(0.5)  # Short delay to ensure LED is on before starting capture
print("Recording... press Ctrl+C to stop.")

button_is_pressed = False

log = {"frames": [], "timestamps": []}

# print("Waiting for voltage trigger on GPIO 4...")
# pause()

# def voltage_triggered():
#     try:
#         frame = cam.capture_array()
#         log["frames"].append(frame)
#         latest_frame_metadata = cam.capture_metadata()
#         log["timestamps"].append(latest_frame_metadata['SensorTimestamp'])               
#         print(f"Timestamp: {log['timestamps'][-1]} ns",end="\r")
#     except KeyboardInterrupt:
#         pass
  

# trigger_pin.when_pressed = voltage_triggered

try:
    while True:
        # request = cam.capture_request()
        # image_frame = request.make_array("main")  # Extracts the image buffer
        # metadata = request.get_metadata()   # Extracts exact metadata for this frame
        # request.release()                   # Always release the request when done
        frame = cam.capture_array()
        timestamp = time.time()-t_trigger
        log["frames"].append(frame)
        # latest_frame_metadata = cam.capture_metadata()
        log["timestamps"].append(timestamp)
        print(f"Timestamp: {log['timestamps'][-1]} s",end="\r")

except KeyboardInterrupt:
    pass
print(len(log["frames"]), len(log["timestamps"]))
# Save the log to a compressed pickle file
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
time.sleep(5)
led.off()    # Turn LED off

print("Done.")