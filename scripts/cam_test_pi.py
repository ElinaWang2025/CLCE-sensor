#!/usr/bin/env python3
"""Pi 3 Camera Module streamer.

Captures frames from the Raspberry Pi Camera (picamera) and streams via
GStreamer using OpenCV's VideoWriter (H264 RTP/UDP). Mirrors behavior
of scripts/cam_test.py but uses the Pi camera input.
"""
import time
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except Exception:
    PiCamera = None
    PiRGBArray = None

import cv2
import numpy as np


def main():
    if PiCamera is None:
        print("Error: picamera not available. Install python-picamera package on the Pi.")
        return

    # Camera settings
    width, height = 640, 480
    fps = 30

    host = "192.168.4.121"
    port = 5000

    gst_pipeline = (
        "appsrc ! videoconvert ! x264enc threads=1 tune=zerolatency bitrate=800 speed-preset=ultrafast ! "
        "rtph264pay config-interval=1 pt=96 ! udpsink host={} port={} sync=false"
    ).format(host, port)

    out = cv2.VideoWriter(gst_pipeline, cv2.CAP_GSTREAMER, 0, float(fps), (width, height), True)
    if not out.isOpened():
        print("Error: Could not open GStreamer pipeline for writing. Ensure OpenCV was built with GStreamer support.")
        return

    print(f"Streaming Pi camera to {host}:{port} via GStreamer udpsink. Press Ctrl+C to stop.")

    camera = PiCamera()
    camera.resolution = (width, height)
    camera.framerate = fps
    raw_capture = PiRGBArray(camera, size=(width, height))

    # Allow camera to warm up
    time.sleep(0.5)

    try:
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            image = frame.array
            if image is None:
                print("Warning: empty frame")
                raw_capture.truncate(0)
                continue

            out.write(image)
            raw_capture.truncate(0)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        out.release()
        camera.close()


if __name__ == "__main__":
    main()
