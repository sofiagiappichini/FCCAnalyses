import torch
import uproot
import numpy as np
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool
import torch.nn.functional as F
from sklearn.model_selection import train_test_split

# === INPUT FILES ===
dir = "/ceph/sgiappic/HiggsCP/CPReco/stage2_explicit_DNN/"
file_even = uproot.open(dir + "EWonly_taudecay_2Pi2Nu.root")["events"]
file_odd = uproot.open(dir + "cehim_m1_taudecay_2Pi2Nu.root")["events"]

# === COMMON VARIABLES TO LOAD ===
# each list will be a node, each node will have 4 features (numbe rof channels int he training) which should be the same in each node
# that's why some are empty for padding import uproot
features_plus1 = ["ZMF_LambdaP_perp_x", "ZMF_LambdaP_perp_y", "ZMF_LambdaP_perp_z", "ZMF_LambdaP_e"]
features_plus2 = ["ZMF_RecoPiP_px", "ZMF_RecoPiP_py", "ZMF_RecoPiP_pz", "ZMF_RecoPiP_e"]
features_min1 = ["ZMF_LambdaM_perp_x", "ZMF_LambdaM_perp_y", "ZMF_LambdaM_perp_z", "ZMF_LambdaM_e"]
features_min2 = ["ZMF_RecoPiM_px", "ZMF_RecoPiM_py", "ZMF_RecoPiM_pz", "ZMF_RecoPiM_e"]
met_features = ["RecoEmiss_px", "RecoEmiss_py", "RecoEmiss_pz", "RecoEmiss_e"]
recoil_feat = ["Recoil_px", "Recoil_py", "Recoil_pz", "Recoil_e"]
ip_feat = ["RecoIP_px", "RecoIP_py", "RecoIP_pz", "OP_ImpactM_e"]
target = "GenPhi_decay"

feature_lists = [features_plus1, features_plus2, features_min1, features_min2, met_features, recoil_feat, ip_feat]
total_features = len(features_plus1)

# === FUNCTION TO LOAD DATA ===
def load_data(tree, cp_label):
    data = {key: tree[key].array(library="np") for key in sum(feature_lists, []) + [target]}
    graphs = []

    for i in range(len(data[target])):
        try:
            p1 = [float(data[f][i]) for f in features_plus2]
            p2 = [float(data[f][i]) for f in features_min2]
            d1 = [float(data[f][i]) for f in features_plus1]
            d2 = [float(data[f][i]) for f in features_min1]
            met = [float(data[f][i]) for f in met_features]
            rec = [float(data[f][i]) for f in recoil_feat]
            ip = [float(data[f][i]) for f in ip_feat]

            x = torch.tensor(np.stack([p1, p2, d1, d2, met, rec, ip], axis=0), dtype=torch.float)

            if x.size(0) < 2:
                continue

            edge_index = torch.combinations(torch.arange(x.size(0)), r=2).T
            edge_index = torch.cat([edge_index, edge_index[[1, 0]]], dim=1)

            phi_star = data[target][i]
            # could use directly the sine and cosine 
            y_reg = torch.tensor([np.sin(phi_star), np.cos(phi_star)], dtype=torch.float).unsqueeze(0)
            y_class = torch.tensor([cp_label], dtype=torch.long)

            graph = Data(x=x, edge_index=edge_index, y_reg=y_reg, y_class=y_class)
            graphs.append(graph)
        except Exception as e:
            print(f"Skipping event {i} due to error: {e}")
            continue
    return graphs

# === LOAD DATA FROM BOTH FILES ===
graphs_even = load_data(file_even, cp_label=0)
graphs_odd = load_data(file_odd, cp_label=1)
all_graphs = graphs_even + graphs_odd

print(f"Graphs loaded: {len(all_graphs)}")
if len(all_graphs) == 0:
    print("Error: No graphs were successfully loaded!")
    exit(1)

# === SPLIT INTO TRAIN/TEST ===
train_graphs, test_graphs = train_test_split(all_graphs, test_size=0.3, random_state=42)
train_loader = DataLoader(train_graphs, batch_size=64, shuffle=True)
test_loader = DataLoader(test_graphs, batch_size=64)

# === GNN Model ===
class TauGNNMultiTask(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels=32):
        super().__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.shared_fc = torch.nn.Linear(hidden_channels, hidden_channels)
        self.reg_head = torch.nn.Linear(hidden_channels, 2)
        self.class_head = torch.nn.Linear(hidden_channels, 2)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, batch)
        x = F.relu(self.shared_fc(x))
        return self.reg_head(x), self.class_head(x)

# === Training & Evaluation Functions ===
# === Training & Evaluation Functions ===
def train(model, loader, optimizer):
    model.train()
    total_loss = 0
    for batch in loader:
        batch = batch.to(device)
        optimizer.zero_grad()
        y_reg_pred, y_class_pred = model(batch)
        
        # Ensure y_reg_pred and batch.y_reg have the same shape
        if y_reg_pred.shape != batch.y_reg.shape:
            raise ValueError(f"Shape mismatch: y_reg_pred {y_reg_pred.shape}, batch.y_reg {batch.y_reg.shape}")
        
        loss_reg = F.mse_loss(y_reg_pred, batch.y_reg)
        loss_class = F.cross_entropy(y_class_pred, batch.y_class.squeeze())
        loss = loss_reg + loss_class
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(loader)

def evaluate(model, loader):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    angle_errors = []

    with torch.no_grad():
        for batch in loader:
            batch = batch.to(device)
            y_reg_pred, y_class_pred = model(batch)
            
            # Ensure y_reg_pred and batch.y_reg have the same shape
            if y_reg_pred.shape != batch.y_reg.shape:
                raise ValueError(f"Shape mismatch: y_reg_pred {y_reg_pred.shape}, batch.y_reg {batch.y_reg.shape}")
            
            loss_reg = F.mse_loss(y_reg_pred, batch.y_reg)
            loss_class = F.cross_entropy(y_class_pred, batch.y_class.squeeze())
            loss = loss_reg + loss_class
            total_loss += loss.item()

            preds = y_class_pred.argmax(dim=1)
            correct += (preds == batch.y_class.squeeze()).sum().item()
            total += batch.num_graphs

            true_phi = torch.atan2(batch.y_reg[:, 0], batch.y_reg[:, 1])
            pred_phi = torch.atan2(y_reg_pred[:, 0], y_reg_pred[:, 1])
            angle_diff = torch.abs((true_phi - pred_phi + np.pi) % (2 * np.pi) - np.pi)
            angle_errors.extend(angle_diff.cpu().numpy())

    acc = correct / total
    mean_angle_err = np.mean(angle_errors)
    return total_loss / len(loader), acc, mean_angle_err

# === Initialize and Train ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = TauGNNMultiTask(in_channels=total_features).to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

print("Training...")
for epoch in range(1, 101):
    train_loss = train(model, train_loader, optimizer)
    val_loss, acc, angle_err = evaluate(model, test_loader)
    print(f"Epoch {epoch:03d} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | "
          f"CP Acc: {acc:.4f} | ⟨|Δφ*|⟩: {angle_err:.4f} rad")
