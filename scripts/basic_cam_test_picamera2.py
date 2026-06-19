from picamera2 import Picamera2
import time

print("Importing done")
camera = Picamera2()
print("Camera object created")

camera.start()
print("Camera started")  # if you never see this, hang is in start()

time.sleep(2)
print("Sleep done")

camera.capture_file("test3.jpg")
print("Captured!")  # if you never see this, hang is in capture_file()

camera.stop()
print("Done")