#!/usr/bin/env python3
"""Pi Camera (libcamera / picamera2) streamer.

Captures frames using picamera2 and streams via GStreamer using OpenCV's
VideoWriter (H264 RTP/UDP). Use this on Raspberry Pi OS with libcamera
and python-picamera2 installed.
"""
import time
try:
    from picamera2 import Picamera2
except Exception:
    Picamera2 = None

import cv2
import numpy as np


def main():
    if Picamera2 is None:
        print("Error: picamera2 not available. Install python-picamera2 on the Pi.")
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

    picam2 = Picamera2()
    config = picam2.create_preview_configuration({"main": {"size": (width, height)}})
    picam2.configure(config)
    picam2.start()

    print(f"Streaming Pi camera (picamera2) to {host}:{port} via GStreamer udpsink. Press Ctrl+C to stop.")

    try:
        while True:
            # capture_array returns RGB by default
            img = picam2.capture_array()
            if img is None:
                print("Warning: empty frame")
                continue

            # Convert RGB -> BGR for OpenCV
            bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            out.write(bgr)
            # small sleep to be cooperative (capture_array is blocking and will limit rate)
            time.sleep(0)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        out.release()
        picam2.stop()


if __name__ == "__main__":
    main()
