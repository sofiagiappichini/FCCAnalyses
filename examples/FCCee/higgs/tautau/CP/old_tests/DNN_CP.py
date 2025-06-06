import uproot
import awkward as ak
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import csv
import matplotlib.pyplot as plt
import os
import torch.nn.functional as F


# Load ROOT tree
def load_data_from_root(file_path, tree_name):
    tree = uproot.open(file_path)[tree_name]
    branches = tree.arrays([
        "OP_ImpactP_px", "OP_ImpactP_py", "OP_ImpactP_pz", "OP_ImpactP_e",
        "OP_ImpactM_px", "OP_ImpactM_py", "OP_ImpactM_pz", "OP_ImpactM_e",
        "ZMF_LambdaP_px", "ZMF_LambdaP_py", "ZMF_LambdaP_pz", "ZMF_LambdaP_e",
        "ZMF_LambdaM_px", "ZMF_LambdaM_py", "ZMF_LambdaM_pz", "ZMF_LambdaM_e",
        "ZMF_LambdaP_perp_x", "ZMF_LambdaP_perp_y", "ZMF_LambdaP_perp_z",
        "ZMF_LambdaM_perp_x", "ZMF_LambdaM_perp_y", "ZMF_LambdaM_perp_z",
        "ZMF_RecoPiP_px", "ZMF_RecoPiP_py", "ZMF_RecoPiP_pz", "ZMF_RecoPiP_e", 
        "ZMF_RecoPiM_px", "ZMF_RecoPiM_py", "ZMF_RecoPiM_pz", "ZMF_RecoPiM_e",
        "RecoPiP_px", "RecoPiP_py", "RecoPiP_pz", "RecoPiP_e", "RecoPiP_phi", "RecoPiP_eta", "RecoPiP_theta", #double
        "RecoPiM_px", "RecoPiM_py", "RecoPiM_pz", "RecoPiM_e", "RecoPiM_phi", "RecoPiM_eta", "RecoPiM_theta", #double
        "RecoIP_px", "RecoIP_py", "RecoIP_pz", #double
        "RecoEmiss_px", "RecoEmiss_py", "RecoEmiss_pz", "RecoEmiss_e", #double
        "Recoil_px", "Recoil_py", "Recoil_pz", "Recoil_e", #double
        "ZMF_px", "ZMF_py", "ZMF_pz", "ZMF_e", #double
        "RecoPiP_D0", "RecoPiP_Z0", "RecoPiM_D0", "RecoPiM_Z0",
        "RecoPiP_charge", "RecoPiM_charge", #int
        "GenPhi_decay", "CosPhi", "SinPhi", #double
    ])
    return branches

# Convert awkward data to numpy feature matrix
def extract_features(events):
    features = []
    truths = []

    num_events = len(events["GenPhi_decay"])

    for i in range(num_events):
        row = []

        # π+ features
        row.extend([
            float(events["RecoPiP_D0"][i]),
            float(events["RecoPiP_Z0"][i]),
            float(events["RecoPiP_phi"][i]),
            float(events["RecoPiP_charge"][i]),
            float(events["RecoPiP_px"][i]),
            float(events["RecoPiP_py"][i]),
            float(events["RecoPiP_pz"][i]),
            float(events["RecoPiP_e"][i]),
            #float(events["ZMF_RecoPiP_px"][i]),
            #float(events["ZMF_RecoPiP_py"][i]),
            #float(events["ZMF_RecoPiP_pz"][i]),
            #float(events["ZMF_RecoPiP_e"][i]),
            #float(events["ZMF_LambdaP_perp_x"][i]),
            #float(events["ZMF_LambdaP_perp_y"][i]),
            #float(events["ZMF_LambdaP_perp_z"][i]),
            #float(events["OP_ImpactP_px"][i]),
            #float(events["OP_ImpactP_py"][i]),
            #float(events["OP_ImpactP_pz"][i]),
            #float(events["OP_ImpactP_e"][i]),
        ])

        # π- features
        row.extend([
            float(events["RecoPiM_D0"][i]),
            float(events["RecoPiM_Z0"][i]),
            float(events["RecoPiM_phi"][i]),
            float(events["RecoPiM_charge"][i]),
            float(events["RecoPiM_px"][i]),
            float(events["RecoPiM_py"][i]),
            float(events["RecoPiM_pz"][i]),
            float(events["RecoPiM_e"][i]),
            #float(events["ZMF_RecoPiM_px"][i]),
            #float(events["ZMF_RecoPiM_py"][i]),
            #float(events["ZMF_RecoPiM_pz"][i]),
            #float(events["ZMF_RecoPiM_e"][i]),
            #float(events["ZMF_LambdaM_perp_x"][i]),
            #float(events["ZMF_LambdaM_perp_y"][i]),
            #float(events["ZMF_LambdaM_perp_z"][i]),
            #float(events["OP_ImpactM_px"][i]),
            #float(events["OP_ImpactM_py"][i]),
            #float(events["OP_ImpactM_pz"][i]),
            #float(events["OP_ImpactM_e"][i]),
        ])

        # Event-level features
        row.extend([
            float(events["RecoIP_px"][i]),
            float(events["RecoIP_py"][i]),
            float(events["RecoIP_pz"][i]),
        ])

        row.extend([
            float(events["ZMF_px"][i]),
            float(events["ZMF_py"][i]),
            float(events["ZMF_pz"][i]),
            float(events["ZMF_e"][i]),
        ])

        row.extend([
            float(events["RecoEmiss_px"][i]),
            float(events["RecoEmiss_py"][i]),
            float(events["RecoEmiss_pz"][i]),
            float(events["RecoEmiss_e"][i]),
        ])

        row.extend([
            float(events["Recoil_px"][i]),
            float(events["Recoil_py"][i]),
            float(events["Recoil_pz"][i]),
            float(events["Recoil_e"][i]),
        ])

        # Append event features to the feature list
        features.append(row)

        # Truth value (phi_star_truth)
        #phi_val = events["GenPhi_decay"][i]
        #truths.append(phi_val)

        # Truth values (sin(phi), cos(phi))
        cos_val = events["CosPhi"][i]
        sin_val = events["SinPhi"][i]
        truths.append([sin_val, cos_val])

    return np.array(features), np.array(truths)

# DNN model
class TauAngleNet(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 2) 
        )

    def forward(self, x):
        return self.net(x)

class TauAngleNet_v1(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        # Predict sin(phi*), cos(phi*)
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),  
            nn.ReLU(),
            nn.Linear(128, 64),         
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, 32),          
            nn.ReLU(),
            nn.Linear(32, 2)            
        )

    def forward(self, x):
        return self.net(x)

class TauAngleNet_v2(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),  
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),            
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        return self.net(x)

class TauAngleNet_v3(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),  
            nn.ReLU(),
            nn.Linear(256, 128),        
            nn.ReLU(),
            nn.Linear(128, 64),         
            nn.ReLU(),
            nn.Linear(64, 48),         
            nn.ReLU(),
            nn.Dropout(0.3),           
            nn.Linear(48, 32),        
            nn.ReLU(),
            nn.Linear(32, 2)          
        )

    def forward(self, x):
        return self.net(x)

class TauAngleNet_v4(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),  
            nn.ReLU(),
            nn.Linear(64, 256),
            nn.ReLU(),
            nn.Dropout(0.5),  
            nn.Linear(256, 128),
            nn.ReLU(),          
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)

class TauAngleNet_v5(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),  
            nn.ReLU(),
            nn.Linear(64, 256),
            nn.ReLU(),
            nn.Dropout(0.4),  
            nn.Linear(256, 512),
            nn.ReLU(),         
            nn.Dropout(0.4),  
            nn.Linear(512, 128),
            nn.ReLU(),          
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)

class TauAngleNetPeriodic(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),  
            nn.Tanh(),
            nn.Linear(64, 128),
            nn.Tanh(),
            nn.Linear(128, 256),
            nn.Tanh(),
            nn.Dropout(0.3),            
            nn.Linear(256, 64),
            nn.Tanh(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        x = self.net(x)
        x = torch.cos(x)
        return x

# Dataset
class TauAngleDatasetPhi(Dataset):
    def __init__(self, features, angles):
        if isinstance(features, torch.Tensor):
            self.X = features.clone().detach()
        else:
            self.X = torch.tensor(features, dtype=torch.float32)

        self.y = torch.tensor(
            np.stack([np.sin(angles), np.cos(angles)], axis=1),
            dtype=torch.float32
        )

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

class TauAngleDataset(Dataset):
    def __init__(self, features, sincos):
        if isinstance(features, torch.Tensor):
            self.X = features.clone().detach()
        else:
            self.X = torch.tensor(features, dtype=torch.float32)

        # sincos should already be a (N, 2) array of [sin(phi), cos(phi)]
        self.y = torch.tensor(sincos, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Training with evaluation on test data and early stopping
def train_model(model, train_loader, X_test, y_test, epochs):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    val_losses = []
    train_losses = []

    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)
    #y_test_tensor = torch.tensor(np.stack([np.sin(y_test), np.cos(y_test)], axis=1), dtype=torch.float32)

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

    '''csv_path = dir + out_csv
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Epoch", "Train_Loss", "Validation_Loss"])
        for i, (t, v) in enumerate(zip(train_losses, val_losses)):
            writer.writerow([i+1, t, v])'''

    plt.figure(figsize=(8, 5))
    plt.plot(train_losses, label="Train Loss", color='indianred')
    plt.plot(val_losses, label="Validation Loss", color='cornflowerblue')
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training vs Validation Loss")
    plt.legend()
    plt.grid(True)
    plot_path = dir + loss_file + ".png"
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved loss plot to: {plot_path}")

    return train_losses, val_losses

# Append the inference to a new root file and plot the histograms
def predidt_plot_root(model, X_array, y_array, input_rootfile, output_file):

    model.eval()
    with torch.no_grad():
        X_tensor = torch.tensor(X_array, dtype=torch.float32)
        pred = model(X_tensor)
        sin_phi, cos_phi = pred[:, 0], pred[:, 1]
        phi_star = torch.atan2(sin_phi, cos_phi).numpy()

    true_cos = y_array[:, 1]
    true_sin = y_array[:, 0]
    true_phi = np.arctan2(true_sin, true_cos)

    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(24, 16))

    bins = 100

    axs[0][0].hist(cos_phi, bins, label="Predicted cosine", color='cornflowerblue')
    axs[0][0].legend()
    axs[0][1].hist(sin_phi, bins, label="Predicted sine", color='cornflowerblue')
    axs[0][1].legend()
    axs[0][2].hist(phi_star, bins, label="Predicted Phi", color='cornflowerblue')
    axs[0][2].legend()

    axs[1][0].scatter(true_cos, cos_phi, label="Predicted vs True cosine", color='cornflowerblue', marker=".", s=2)
    axs[1][1].scatter(true_sin, sin_phi, label="Predicted vs True sine", color='cornflowerblue', marker=".", s=2)
    axs[1][2].scatter(true_phi, phi_star, label="Predicted vs True Phi", color='cornflowerblue', marker=".", s=2)
    
    axs[1][0].plot([min(true_cos), max(true_cos)], [min(true_cos), max(true_cos)], linestyle='--', color='indianred')
    axs[1][0].legend()
    axs[1][1].plot([min(true_sin), max(true_sin)], [min(true_sin), max(true_sin)], linestyle='--', color='indianred')
    axs[1][1].legend()
    axs[1][2].plot([min(true_phi), max(true_phi)], [min(true_phi), max(true_phi)], linestyle='--', color='indianred')
    axs[1][2].legend()

    plt.tight_layout()
    plot_path = dir + plot_file + ".png"
    plt.savefig(plot_path)

    with uproot.open(input_rootfile) as file:
        tree = file["events"]
        data = tree.arrays(library="np")  

    data["DNN_PhiCP"] = phi_star
    data["DNN_CosCP"] = sin_phi
    data["DNN_SinCP"] = cos_phi
    selected_keys = ["PhiCP_CMS", "GenPhi_decay", "DNN_PhiCP", "DNN_CosCP", "DNN_SinCP"]
    filtered_data = {key: data[key] for key in selected_keys if key in data}

    with uproot.recreate(output_file) as new_file:
        new_file["events"] = filtered_data

    print(f"New ROOT file created: {output_file}")

# Modify the append function to save predictions to CSV instead of ROOT
def append_predictions_to_csv(model, X_array, output_csv_file):
    model.eval()
    with torch.no_grad():
        X_tensor = torch.tensor(X_array, dtype=torch.float32)
        pred = model(X_tensor)
        sin_phi, cos_phi = pred[:, 0], pred[:, 1]
        phi_star = torch.atan2(sin_phi, cos_phi).numpy()
    
    with open(output_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["EventIndex", "PredictedPhiStar"])
        for i, pred in enumerate(phi_star):
            writer.writerow([i, pred])
    print(f"Predictions have been saved to {output_csv_file}")

# Function to plot predictions vs true values for the test set
def plot_predictions_vs_true(model, X_test, y_test, dir):
    model.eval()
    with torch.no_grad():
        X_tensor = torch.tensor(X_test, dtype=torch.float32)
        pred = model(X_tensor)
        sin_phi, cos_phi = pred[:, 0], pred[:, 1]
        pred_phi_star = torch.atan2(sin_phi, cos_phi).numpy()

    plt.figure(figsize=(8, 5))
    plt.scatter(y_test, pred_phi_star, color='cornflowerblue', label='Predicted vs True', marker=".", s=2)
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], linestyle='--', label='Perfect Prediction', color='indianred' )
    plt.xlabel('True Phi')
    plt.ylabel('Predicted Phi')
    plt.title('Predicted vs True Phi for Test Set')
    plt.legend()
    plot_path = dir + plot_file + ".png"
    plt.savefig(plot_path)

# Run everything
dir = "/ceph/sgiappic/HiggsCP/CPReco/stage2_explicit_DNN/"
rootfile = dir + "EWonly_taudecay_2Pi2Nu.root"
out = dir + "EWonly_taudecay_2Pi2Nu_DNN_periodic.root"
model_name = "HiggsCP_DNN_model_periodic"
plot_file = "prediction_plot_periodic"
loss_file = "loss_plot_periodic"
array_path = "EWonly_taudecay_2Pi2Nu_Numpy"
path = dir + array_path + ".npz"
treename = "events"

train = True
apply = False

if train:

    if os.path.exists(path):
        print("Importing arrays")
        data = np.load(path)
        X = data['features']
        y_phi_star = data['truths']

    else:
        print("Load tree")
        events = load_data_from_root(rootfile, treename)
        X, y_phi_star = extract_features(events)
        np.savez(path, features=np.array(X), truths=np.array(y_phi_star))

    # Get input dimension automatically
    input_dim = X.shape[1]
    
    print("Split data into 30% training and 70% testing")
    X_train, X_test, y_train, y_test = train_test_split(X, y_phi_star, test_size=0.3, random_state=42)

    print("Convert training data to PyTorch tensors")
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    #y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

    print("Create DataLoader for training")
    train_dataset = TauAngleDataset(X_train_tensor, y_train)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    print("Initialize and train the model")
    model = TauAngleNetPeriodic(input_dim)
    train_losses, val_losses = train_model(model, train_loader, X_test, y_test, epochs=400)

    print(f"Save model to {dir}")
    torch.save(model, dir + model_name + '.pth')

    #print("Plot the predicted values for the test dataset")
    #plot_predictions_vs_true(model, X_test, y_test, dir)

    print("Predict on the entire dataset")
    #append_predictions_to_csv(model, X, out_csv)
    predidt_plot_root(model, X, y_phi_star, rootfile, out)

if apply:
    
    print("Load model")
    model = torch.load(dir + model_name + '.pth')

    print("Importing arrays")
    data = np.load(path)
    X = data['features']
    y = data['truths']

    #print("Plot the predicted values for the test dataset")
    #plot_predictions_vs_true(model, X, y, dir)

    print("Predict on the entire dataset")
    #append_predictions_to_csv(model, X, out_csv)
    predidt_plot_root(model, X, y, rootfile, out)