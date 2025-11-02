import bvhio
import json
import os

def convert_bvh_to_json(bvh_filename, json_filename):
    """
    Reads a .bvh file and converts its motion data into our simple JSON format.
    """
    print(f"Starting conversion for: {bvh_filename}")

    try:
        # bvh_data is the ROOT JOINT of the hierarchy
        bvh_data = bvhio.readAsHierarchy(bvh_filename)
    except Exception as e:
        print(f"Error reading BVH file {bvh_filename}: {e}")
        return

    all_frames_data = []
    
    joint_names = [joint.Name for joint, index, depth in bvh_data.layout()]

    # --- !!! THIS IS THE FIX !!! ---
    # 1. Get the frame range from the root joint
    start_frame, end_frame = bvh_data.getKeyframeRange()
    
    # 2. Calculate the total frame count
    frame_count = end_frame + 1
    
    # 3. Use the correct frame_count variable in our "flag" print
    print(f"File loaded. Found {len(joint_names)} joints. Processing {frame_count} frames...")

    # --- 4. Loop from 0 up to the frame_count ---
    for frame_index in range(frame_count):
        
        frame_pose = {}
        
        # This loads the pose for the specified frame index
        bvh_data.loadPose(frame_index)

        for joint, index, depth in bvh_data.layout():
            
            quat = joint.Rotation
            
            frame_pose[joint.Name] = { 
                "x": quat[0],
                "y": quat[1],
                "z": quat[2],
                "w": quat[3]
            }
        all_frames_data.append(frame_pose)

    # --- 5. Save the final JSON file ---
    output_data = {
        "jointNames": joint_names,
        "frames": all_frames_data
    }

    try:
        output_path = os.path.join('static', json_filename)
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=4)
        
        print(f"SUCCESS! Saved JSON to: {output_path}")
        print("-----------------------------------")
        
    except Exception as e:
        print(f"Error writing JSON file: {e}")

# --- 6. Run the conversion ---
if __name__ == "__main__":
    convert_bvh_to_json('T-pose.bvh', 't-pose.json')
    convert_bvh_to_json('Walking.bvh', 'walking.json')