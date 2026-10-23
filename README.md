# CLCE-sensor

This project interfaces with a camera

## Installation

Setup virtual environment for this repo

```sh
uv venv
source .venv/bin/activate
uv pip install numpy 
# sudo apt update
# sudo apt install -y gstreamer1.0-tools gstreamer1.0-plugins-base \
# gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
# libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
# gstreamer1.0-libcamera
# Force pip to build from source distribution and inject the GStreamer flag
# export CMAKE_ARGS="-DWITH_GSTREAMER=ON -DWITH_GSTREAMER_0_10=OFF"
uv pip install --no-binary opencv-python opencv-python

```


on laptop stream
```sh
gst-launch-1.0 udpsrc port=5000 ! application/x-rtp, payload=96 ! rtph264depay ! decodebin ! autovideosink
```

running on pi5
```sh
source /home/cee/CLCE-sensor/.venv/bin/activate
```
