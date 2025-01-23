import os
import subprocess
import random

def display_models_in_path(folder_path):
    """
    Displays the models in the specified folder path in a paginated, two-column layout.
    """
    files = [f for f in os.listdir(folder_path) if f.endswith('.safetensors')]
    files.sort()
    if not files:
        print("No `.safetensors` files found in the specified path.")
        return None

    current_index = 0
    page_size = 50

    while current_index < len(files):
        page_files = files[current_index:current_index + page_size]
        column1 = page_files[:len(page_files) // 2]
        column2 = page_files[len(page_files) // 2:]

        print("\nModels:")
        for i in range(max(len(column1), len(column2))):
            left = f"{current_index + i + 1}: {column1[i]}" if i < len(column1) else ""
            right = f"{current_index + len(column1) + i + 1}: {column2[i]}" if i < len(column2) else ""
            print(f"{left:<40} {right}")

        current_index += page_size
        if current_index < len(files):
            input("\nPress Enter to view the next page...")

    return files

def random_loras_and_weights(folder_path, count):
    """
    Selects random LoRAs from the folder and generates random weights summing to 1.0,
    rounded to two decimal places.
    """
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.safetensors')]
    if len(files) < count:
        print(f"Error: Only {len(files)} LoRAs available, but {count} required.")
        return None, None

    selected_files = random.sample(files, count)
    weights = [random.random() for _ in range(count)]
    total_weight = sum(weights)
    normalized_weights = [round(w / total_weight, 2) for w in weights]

    # Adjust the last weight to ensure the sum equals exactly 1.0
    normalized_weights[-1] = round(1.0 - sum(normalized_weights[:-1]), 2)

    return selected_files, normalized_weights

def run_flux_merge_random():
    """
    Runs Flux Merge with random LoRAs and weights.
    """
    script_path = r"H:\sd-scripts\networks\flux_merge_lora.py"
    if not os.path.exists(script_path):
        print(f"Error: The script '{script_path}' does not exist.")
        return

    lora_count = int(input("Enter the number of LoRAs to use: ").strip())
    folder_path = input("Enter the path to the folder containing LoRA models: ").strip()

    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    selected_files, normalized_weights = random_loras_and_weights(folder_path, lora_count)
    if not selected_files:
        return

    precision = input("Enter the precision (e.g., fp16 or fp32): ").strip()
    save_to = input("Enter the path to save the merged LoRA file (e.g., C:\\output.safetensors): ").strip()

    command = [
        "python", script_path,
        "--precision", precision,
        "--save_precision", precision,
        "--save_to", save_to,
        "--models", *selected_files,
        "--ratios", *map(str, normalized_weights),
        "--diffusers", "--shuffle", "--no_metadata"
    ]

    print("\nGenerated Command:")
    print(" ".join(command))
    run_command = input("Do you want to run this command? (yes/no): ").strip().lower()

    if run_command == "yes":
        print("Running the command...")
        subprocess.run(command)
        print("Flux Merge completed.")
    else:
        print("Command not executed.")

def run_svd_merge_random():
    """
    Runs SVD Merge with random LoRAs and weights.
    """
    script_path = r"H:\sd-scripts\networks\svd_merge_lora.py"
    if not os.path.exists(script_path):
        print(f"Error: The script '{script_path}' does not exist.")
        return

    lora_count = int(input("Enter the number of LoRAs to use: ").strip())
    folder_path = input("Enter the path to the folder containing LoRA models: ").strip()

    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    selected_files, normalized_weights = random_loras_and_weights(folder_path, lora_count)
    if not selected_files:
        return

    save_to = input("Enter the path to save the merged LoRA file (e.g., H:\\output.safetensors): ").strip()

    command = [
        "python", script_path,
        "--save_to", save_to,
        "--models", *selected_files,
        "--ratios", *map(str, normalized_weights),
        "--no_metadata"
    ]

    print("\nGenerated Command:")
    print(" ".join(command))
    run_command = input("Do you want to run this command? (yes/no): ").strip().lower()

    if run_command == "yes":
        print("Running the command...")
        subprocess.run(command)
        print("SVD Merge completed.")
    else:
        print("Command not executed.")

def run_flux_merge():
    """
    Runs the Flux Merge script with user-defined parameters.
    """
    script_path = r"H:\sd-scripts\networks\flux_merge_lora.py"
    if not os.path.exists(script_path):
        print(f"Error: The script '{script_path}' does not exist.")
        return

    folder_path = input("Enter the path to the folder containing the LoRA models: ").strip()
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    files = display_models_in_path(folder_path)
    if not files:
        return

    selected_models, selected_ratios = ask_user_for_models(folder_path, files)

    precision = input("Enter the precision (e.g., fp16 or fp32): ").strip()
    save_to = input("Enter the path to save the merged LoRA file (e.g., C:\\output.safetensors): ").strip()

    model_list = " ".join(selected_models)
    ratio_list = " ".join(map(str, selected_ratios))
    command = [
        "python", script_path,
        "--precision", precision,
        "--save_precision", precision,
        "--save_to", save_to,
        "--models", *selected_models,
        "--ratios", *map(str, selected_ratios),
        "--diffusers", "--shuffle", "--no_metadata"
    ]

    print("\nGenerated Command:")
    print(" ".join(command))
    run_command = input("Do you want to run this command? (yes/no): ").strip().lower()

    if run_command == "yes":
        print("Running the command...")
        subprocess.run(command)
        print("Flux Merge completed.")
    else:
        print("Command not executed.")

def run_svd_merge():
    """
    Runs the SVD Merge script with user-defined parameters.
    """
    script_path = r"H:\sd-scripts\networks\svd_merge_lora.py"
    if not os.path.exists(script_path):
        print(f"Error: The script '{script_path}' does not exist.")
        return

    folder_path = input("Enter the path to the folder containing the LoRA models: ").strip()
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    files = display_models_in_path(folder_path)
    if not files:
        return

    selected_models, selected_ratios = ask_user_for_models(folder_path, files)

    save_to = input("Enter the path to save the merged LoRA file (e.g., H:\\saveto.safetensors): ").strip()

    model_list = " ".join(selected_models)
    ratio_list = " ".join(map(str, selected_ratios))
    command = [
        "python", script_path,
        "--save_to", save_to,
        "--models", *selected_models,
        "--ratios", *map(str, selected_ratios),
        "--no_metadata"
    ]

    print("\nGenerated Command:")
    print(" ".join(command))
    run_command = input("Do you want to run this command? (yes/no): ").strip().lower()

    if run_command == "yes":
        print("Running the command...")
        subprocess.run(command)
        print("SVD Merge completed.")
    else:
        print("Command not executed.")

def ask_user_for_models(folder_path, files):
    """
    Guides the user to select models and their respective ratios.
    """
    selected_models = []
    selected_ratios = []
    while True:
        print("\nSelect a model by entering its number from the list above:")
        try:
            model_index = int(input("Model number: ").strip()) - 1
            if model_index < 0 or model_index >= len(files):
                print("Invalid selection. Please try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        model_path = os.path.join(folder_path, files[model_index])
        print(f"Selected model: {model_path}")
        ratio = input(f"Enter the weight (ratio) for {model_path} (e.g., 0.33): ").strip()

        try:
            ratio = float(ratio)
            if ratio <= 0 or ratio > 1:
                print("Ratio must be greater than 0 and less than or equal to 1.")
                continue
        except ValueError:
            print("Invalid ratio. Please enter a numeric value.")
            continue

        selected_models.append(model_path)
        selected_ratios.append(ratio)

        if len(selected_models) >= 2:
            more_models = input("Do you want to add another model? (yes/no): ").strip().lower()
            if more_models != "yes":
                break

    return selected_models, selected_ratios

def main_menu():
    """
    Main menu providing options for merging and quitting.
    """
    while True:
        print("\nLoRA Model Merger Menu")
        print("1. Kohya Flux LoRA Merge - Flux Merge Script")
        print("2. SVD LoRA Merge - SVD Merge Script")
        print("3. Random Kohya Flux LoRA Merge - Random LoRAs with Random Weights")
        print("4. Random SVD LoRA Merge - Random LoRAs with Random Weights")
        print("5. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            run_flux_merge()
        elif choice == "2":
            run_svd_merge()
        elif choice == "3":
            run_flux_merge_random()
        elif choice == "4":
            run_svd_merge_random()
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
