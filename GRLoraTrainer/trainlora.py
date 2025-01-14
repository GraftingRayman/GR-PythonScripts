import os
import subprocess
from pathlib import Path
import re
from datetime import datetime
import threading

def main():
    print("Welcome to Flux1 Training Automation")

    # Prompt the user for the dataset directory
    dataset_path = input("Enter the full path to the dataset (e.g., c:\\images\\circles\\5_circles): ").strip()

    # Ensure dataset path exists
    if not os.path.exists(dataset_path):
        print(f"Error: The specified dataset path '{dataset_path}' does not exist.")
        return

    # Automatically use the parent directory of the input path
    parent_directory = str(Path(dataset_path).parent)
    dataset_folder_name = Path(dataset_path).name  # Extract the folder name (e.g., "5_circles")
    print(f"Using parent directory for training data: {parent_directory}")
    print(f"Dataset folder name extracted: {dataset_folder_name}")

    # Extract the number of digits from the dataset folder name
    digit_match = re.search(r"(\d+)_", dataset_folder_name)
    if not digit_match:
        print("Error: Unable to extract the number of digits from the dataset folder name.")
        return

    dataset_digits = int(digit_match.group(1))

    # Count the number of images in the provided directory
    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    image_files = [f for f in Path(dataset_path).iterdir() if f.suffix.lower() in valid_exts]
    number_of_images = len(image_files)

    if number_of_images == 0:
        print("Error: No valid images found in the specified dataset directory.")
        return

    print(f"Found {number_of_images} images in the dataset directory: {dataset_path}.")

    # Prompt the user for resolution
    resolution_options = {"1": "512", "2": "768", "3": "1024"}
    resolution = None
    while resolution not in resolution_options:
        print("Select the resolution:")
        print("1. 512")
        print("2. 768")
        print("3. 1024")
        resolution = input("Enter 1, 2, or 3: ").strip()
        if resolution not in resolution_options:
            print("Invalid choice. Please select 1, 2, or 3.")

    # Get the selected resolution value
    selected_resolution = resolution_options[resolution]

    # Prompt the user for sample generation steps with a timeout
    generate_sample_steps = get_user_input_with_timeout(
        "Enter the sample generation interval in steps (default: 250): ", 250, 30
    )
    print(f"Using sample generation interval: {generate_sample_steps}")

    # Set the number of epochs to 16
    epochs = 16
    max_train_steps = number_of_images * epochs * dataset_digits

    # Set the save frequency to 500
    save_every_n_steps = 500

    # Define fixed paths
    repo_path = "H:\\sd-scripts"
    flux_train_script = os.path.join(repo_path, "flux_train_network.py")
    base_model_path = "E:\\models\\flux1-dev.safetensors"
    ae_path = "E:\\models\\ae.safetensors"
    clip_model_path = "E:\\models\\clip_l.safetensors"
    t5_model_path = "E:\\models\\t5xxl_fp16.safetensors"

    # Create the configuration file in the parent folder
    config_file_path = os.path.join(parent_directory, "config.toml")
    config_content = f"""[general]
shuffle_caption = false
caption_extension = '.txt'
keep_tokens = 1

[[datasets]]
batch_size = 1
keep_tokens = 1
resolution = {selected_resolution}

  [[datasets.subsets]]
  image_dir = '{dataset_path}'
  class_tokens = ''
  num_repeats = {dataset_digits}

"""

    with open(config_file_path, "w") as config_file:
        config_file.write(config_content)

    print(f"Configuration file created: {config_file_path}")

    # Build the training command
    command = [
        "python", flux_train_script,
        f"--pretrained_model_name_or_path={base_model_path}",
        f"--ae={ae_path}",
        f"--output_dir={parent_directory}",
        f"--output_name={dataset_folder_name}",
        f"--train_data_dir={parent_directory}",
        f"--dataset_config={config_file_path}",  # Add the dataset_config argument
        f"--learning_rate=8e-4",
        f"--max_train_steps={max_train_steps}",
        f"--save_every_n_steps={save_every_n_steps}",
        f"--save_model_as=safetensors",
        f"--logging_dir=logs",
        f"--clip_l={clip_model_path}",
        f"--t5xxl={t5_model_path}",
        f"--resolution={selected_resolution}",
        f"--sample_every_n_steps={generate_sample_steps}",
        f"--network_module=networks.lora_flux",
        f"--network_dim=4",
        "--cache_text_encoder_outputs",
        "--cache_text_encoder_outputs_to_disk",
        "--fp8_base",
        "--highvram",
        "--max_train_epochs=16",
        "--save_every_n_epochs=1",
        "--cache_latents_to_disk",
        "--sdpa",
        "--persistent_data_loader_workers",
        "--max_data_loader_n_workers=2",
        "--seed=42",
        "--gradient_checkpointing",
        "--mixed_precision=bf16",
        "--save_precision=bf16",
        "--network_train_unet_only",
        "--timestep_sampling=shift",
        "--discrete_flow_shift=3.1582",
        "--model_prediction_type=raw",
        "--guidance_scale=1.0",
        "--sample_prompts=e:\\models\\sample_prompts.txt",
        "--save_state"
    ]

    # Print the command to verify
    print("\nGenerated training command:")
    print(" ".join(command))

    # Confirm execution
    confirm = input("\nDo you want to execute this command? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        # Run the command
        subprocess.run(command)
    else:
        print("Training aborted by the user.")

if __name__ == "__main__":
    main()
