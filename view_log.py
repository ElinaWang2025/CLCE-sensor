import gzip
import pickle
import sys
import matplotlib.pyplot as plt

# Run as `python3 view_log.py <log_file.pkl.gz>`
with gzip.open(sys.argv[1], "rb") as f:
    log = pickle.load(f)
    print(f"Loaded log with {len(log['frames'])} frames and {len(log['timestamps'])} timestamps.")

image_data = log['frames'][0]  # Get the first frame for visualization
plt.imshow(image_data)
plt.title(log['timestamps'][0])
plt.show()