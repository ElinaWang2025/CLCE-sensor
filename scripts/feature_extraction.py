# Step 2: Feature Extraction on a PC (one-time)
# Run this on your PC/Mac, not the Pi. Extract DINOv3 embeddings 
# for every image and save them — this way you never need to run the 
# full backbone again during training or (optionally) inference.


import torch
import numpy as np
from pathlib import Path
from PIL import Image
from transformers import AutoImageProcessor, AutoModel

device = "cuda" if torch.cuda.is_available() else "cpu"

model_name = "facebook/dinov3-vits16-pretrain-lvd1689m"
processor = AutoImageProcessor.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device).eval()

data_dir = Path("data")
embeddings, labels = [], []

for img_path in sorted(data_dir.glob("*.jpg")):
    force = float(img_path.stem.split("_")[0])
    image = Image.open(img_path).convert("RGB")
    
    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.inference_mode():
        outputs = model(**inputs)
    
    # CLS token — shape (768,) for ViT-S
    emb = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
    embeddings.append(emb)
    labels.append(force)

np.save("embeddings.npy", np.array(embeddings))
np.save("labels.npy", np.array(labels))
print(f"Saved {len(labels)} samples")