import os
from pathlib import Path
import torch

def merge_lora_files():
    print("LoRA Model Merger")

    # Prompt for the first LoRA file
    lora1_path = input("Enter the path to the first LoRA file: ").strip()
    if not os.path.exists(lora1_path):
        print(f"Error: File '{lora1_path}' does not exist.")
        return

    # Prompt for the second LoRA file
    lora2_path = input("Enter the path to the second LoRA file: ").strip()
    if not os.path.exists(lora2_path):
        print(f"Error: File '{lora2_path}' does not exist.")
        return

    # Load the LoRA files
    try:
        print("Loading LoRA files...")
        lora1 = torch.load(lora1_path, map_location="cpu")
        lora2 = torch.load(lora2_path, map_location="cpu")
    except Exception as e:
        print(f"Error loading LoRA files: {e}")
        return

    # Merge the models
    print("Merging LoRA models...")
    merged_lora = {}
    for key in lora1.keys():
        if key in lora2:
            merged_lora[key] = (lora1[key] + lora2[key]) / 2
        else:
            merged_lora[key] = lora1[key]

    for key in lora2.keys():
        if key not in merged_lora:
            merged_lora[key] = lora2[key]

    # Create the name for the new LoRA file
    lora1_name = Path(lora1_path).stem
    lora2_name = Path(lora2_path).stem
    new_lora_name = f"{lora1_name}_and_{lora2_name}.safetensors"

    # Save the merged LoRA file
    try:
        output_dir = Path("./merged_lora")
        output_dir.mkdir(exist_ok=True)
        new_lora_path = output_dir / new_lora_name
        torch.save(merged_lora, new_lora_path)
        print(f"Merged LoRA file saved as: {new_lora_path}")
    except Exception as e:
        print(f"Error saving merged LoRA file: {e}")

if __name__ == "__main__":
    merge_lora_files()
