# Step 3: Train the Regression Head (on PC or Mac)
# Step 4: Deploy only the regression head
# Pre-extract embeddings on a PC, copy force_regressor.pth to the Pi, 
# and run only the tiny MLP on-device. This is extremely fast (~1ms inference).

import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split

X = torch.tensor(np.load("embeddings.npy"), dtype=torch.float32)
y = torch.tensor(np.load("labels.npy"), dtype=torch.float32).unsqueeze(1)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

class ForceRegressor(nn.Module):
    def __init__(self, input_dim=384):  # 384 for ViT-S, 768 for ViT-B
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x):
        return self.net(x)

model = ForceRegressor(input_dim=384)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

for epoch in range(200):
    model.train()
    pred = model(X_train)
    loss = loss_fn(pred, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        model.eval()
        with torch.no_grad():
            val_loss = loss_fn(model(X_val), y_val).item() ** 0.5
        print(f"Epoch {epoch} | Val RMSE: {val_loss:.4f} N")

torch.save(model.state_dict(), "force_regressor.pth")