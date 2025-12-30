import numpy as np
import json
import torch

# --- SETTINGS ---
NPY_PATH = "outputs/results.npy"
JSON_PATH = "outputs/motion.json" # Use v2 to bypass cache
MEAN_PATH = "./exit/t2m-mean.npy"
STD_PATH  = "./exit/t2m-std.npy"

def main():
    print(f"🔹 Loading {NPY_PATH}...")
    try:
        data = np.load(NPY_PATH)
        mean = np.load(MEAN_PATH)
        std = np.load(STD_PATH)
    except FileNotFoundError:
        print("❌ Error: Missing files.")
        return

    # 1. DENORMALIZE
    if len(data.shape) == 3:
        data = data[0]
    
    # Unzip the data
    data = (data * std) + mean
    data_tensor = torch.tensor(data).float()
    frames = data.shape[0]

    # 2. RECOVER ROOT (Trajectory)
    r_pos = torch.zeros((frames, 3)).float()
    
    # Calculate X/Z Trajectory from Velocity
    r_pos[1:, 0] = data_tensor[:-1, 1] # Vel X
    r_pos[1:, 2] = data_tensor[:-1, 2] # Vel Z
    r_pos = torch.cumsum(r_pos, dim=0)
    
    # Root Height (Channel 3)
    r_pos[:, 1] = data_tensor[:, 3]

    # 3. RECOVER JOINTS
    # Channels 4 to 67 are the 21 joints
    positions = data_tensor[:, 4:67].reshape(frames, 21, 3)
    
    # --- THE FIX IS HERE ---
    # We add Root X and Z to make the character walk.
    # We do NOT add Root Y, because the AI's Y-channel is already "Absolute Height".
    
    positions[:, :, 0] += r_pos[:, 0:1] # Add Root X
    # positions[:, :, 1] += r_pos[:, 1:2] <--- DELETED THIS LINE (The Bug)
    positions[:, :, 2] += r_pos[:, 2:3] # Add Root Z

    # 4. SAVE
    animation_data = []
    r_pos_np = r_pos.numpy()
    positions_np = positions.numpy()

    for f in range(frames):
        frame_joints = []
        
        # Joint 0: Root
        root = r_pos_np[f]
        frame_joints.append([float(root[0]), float(root[1]), float(root[2])])
        
        # Joints 1-21
        for j in range(21):
            joint = positions_np[f, j]
            frame_joints.append([float(joint[0]), float(joint[1]), float(joint[2])])
            
        animation_data.append(frame_joints)

    output = { "fps": 20, "total_frames": frames, "frames": animation_data }
    with open(JSON_PATH, 'w') as f:
        json.dump(output, f)

    print(f"✅ SUCCESS! Fixed Double-Height Bug. Saved to: {JSON_PATH}")

if __name__ == "__main__":
    main()