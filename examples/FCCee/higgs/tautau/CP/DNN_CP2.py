import uproot
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt

dir = "/ceph/sgiappic/HiggsCP/CPReco/stage2_explicit_DNN/"
cp_even_file = uproot.open(dir + "EWonly_taudecay_2Pi2Nu.root")
cp_odd_file = uproot.open(dir + "cehim_m1_taudecay_2Pi2Nu.root")

cp_even_tree = cp_even_file['events']
cp_odd_tree = cp_odd_file['events']

features = [
    #"RecoPiP_px", "RecoPiP_py", "RecoPiP_pz", "RecoPiP_e", "RecoPiP_phi", "RecoPiP_eta", "RecoPiP_theta", 
    #"RecoPiM_px", "RecoPiM_py", "RecoPiM_pz", "RecoPiM_e", "RecoPiM_phi", "RecoPiM_eta", "RecoPiM_theta", 
    "ZMF_LambdaP_perp_x", "ZMF_LambdaP_perp_y", "ZMF_LambdaP_perp_z",
    "ZMF_LambdaM_perp_x", "ZMF_LambdaM_perp_y", "ZMF_LambdaM_perp_z",
    "ZMF_RecoPiP_px", "ZMF_RecoPiP_py", "ZMF_RecoPiP_pz", "ZMF_RecoPiP_e", 
    "ZMF_RecoPiM_px", "ZMF_RecoPiM_py", "ZMF_RecoPiM_pz", "ZMF_RecoPiM_e",
    "RecoIP_px", "RecoIP_py", "RecoIP_pz", 
    "RecoEmiss_px", "RecoEmiss_py", "RecoEmiss_pz", "RecoEmiss_e", 
    "Recoil_px", "Recoil_py", "Recoil_pz", "Recoil_e", 
    #"RecoPiP_D0", "RecoPiP_Z0", "RecoPiM_D0", "RecoPiM_Z0",
    ]

cp_even_df = cp_even_tree.arrays(features, library="pd")
cp_odd_df = cp_odd_tree.arrays(features, library="pd")

# Add labels for CP even (0) and CP odd (1)
cp_even_df['label'] = 0
cp_odd_df['label'] = 1

# Combine the dataframes
df = pd.concat([cp_even_df, cp_odd_df], ignore_index=True)
df = df.sample(frac=1).reset_index(drop=True)

X = df[features].values
y = df['label'].values

print(df['label'].value_counts())

# Standardize the features (mean 0 and standard deviation 1 so the model is not influenced)
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=42)

class DNNModel(nn.Module):
    def __init__(self, input_size):
        super(DNNModel, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, 32)
        self.fc5 = nn.Linear(32, 1) 
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.relu(self.fc4(x))
        x = self.fc5(x)  
        return x

model = DNNModel(input_size=X_train.shape[1])

criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)  # Reshape for binary classification
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Train the Model ---
epochs = 100
val_losses = []
train_losses = []
for epoch in range(epochs):
        model.train()
        total_train_loss = 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            pred = model(X_batch)
            loss = criterion(pred, y_batch)
            loss.backward()
            optimizer.step()
            total_train_loss += loss.item()

        model.eval()
        with torch.no_grad():
            val_pred = model(X_test_tensor)
            val_loss = criterion(val_pred, y_test_tensor).item()

        avg_train_loss = total_train_loss / len(train_loader)
        train_losses.append(avg_train_loss)
        val_losses.append(val_loss)

        print(f"Epoch {epoch+1:03d} | Train Loss: {avg_train_loss:.6f} | Val Loss: {val_loss:.6f}")

# Plot the loss
plt.figure(figsize=(8, 5))
plt.plot(train_losses, label="Train Loss", color='indianred')
plt.plot(val_losses, label="Validation Loss", color='cornflowerblue')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()
plt.grid(True)
plot_path = dir + "plot_loss.png"
plt.savefig(plot_path)
plt.close()

# Evaluate the Model
model.eval()
with torch.no_grad():
    y_pred = torch.sigmoid(model(X_test_tensor)) # Probability

y_pred_np = y_pred.numpy().flatten()

plt.figure(figsize=(8, 5))
plt.hist(y_pred_np[y_test == 0], bins=50, alpha=0.7, label="CP-even (true)", color='mediumseagreen')
plt.hist(y_pred_np[y_test == 1], bins=50, alpha=0.7, label="CP-odd (true)", color='steelblue')
plt.xlabel("Predicted CP-odd Probability")
plt.ylabel("Number of Events")
plt.title("Predicted CP-odd Probability Distribution")
plt.legend()
plot_path = dir + "plot_pred.png"
plt.savefig(plot_path)
plt.close()

