import time
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from gpiozero import LED

led = LED(18)
led.on()

picam2 = Picamera2()
video_config = picam2.create_video_configuration(main={"size": (224, 224)})
picam2.configure(video_config)

# 1. Define the encoder and the output destination separately
encoder = H264Encoder()
output_destination = FfmpegOutput("output.mp4")

# 2. Pass both arguments into start_recording
picam2.start_recording(encoder, output_destination)

print("Recording started...")
time.sleep(10) 

picam2.stop_recording()
led.off()
print("Recording stopped and saved successfully as output.mp4")