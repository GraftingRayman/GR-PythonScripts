import os
import subprocess

def run_train_lora():
    train_lora_script = "trainlora.py"
    if not os.path.exists(train_lora_script):
        print(f"Error: The script '{train_lora_script}' does not exist.")
        return

    print("Running trainlora.py...")
    subprocess.run(["python", train_lora_script])

def run_caption():
    caption_script = "caption.py"
    if not os.path.exists(caption_script):
        print(f"Error: The script '{caption_script}' does not exist.")
        return

    folder_path = input("Enter the folder path containing images to caption: ").strip()
    print("Running caption.py...")
    subprocess.run(["python", caption_script, folder_path])

def run_resume_lora():
    resume_lora_script = "resume.py"
    if not os.path.exists(resume_lora_script):
        print(f"Error: The script '{resume_lora_script}' does not exist.")
        return

    print("Running resume.py...")
    subprocess.run(["python", resume_lora_script])

def run_merge_lora():
    merge_lora_script = "mergelora.py"
    if not os.path.exists(merge_lora_script):
        print(f"Error: The script '{merge_lora_script}' does not exist.")
        return

    print("Running mergelora.py...")
    subprocess.run(["python", merge_lora_script])

def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Run Captioning Script")
        print("2. Train LoRA (Flux1 Training)")
        print("3. Resume LoRA Training")
        print("4. Merge LoRA Models")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            run_caption()
        elif choice == "2":
            run_train_lora()
        elif choice == "3":
            run_resume_lora()
        elif choice == "4":
            run_merge_lora()
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
