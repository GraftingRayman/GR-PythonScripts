import sys
from pathlib import Path
import shutil
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def caption_images_in_folder(folder_path):
    """
    For each image in 'folder_path', generate a caption with BLIP,
    then write it to a .txt file with the same basename.
    After captioning, move the images and captions to a subfolder with a user-specified prefix.
    """
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"\n'{folder_path}' is not a valid directory.")
        return

    try:
        repeat_number = int(input("Enter the number to prefix the folder name (e.g., 10): "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    # Determine the device early
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Prompt user to select a BLIP model
    print("\nSelect a BLIP model:")
    print("1. BLIP Base (Salesforce/blip-image-captioning-base)")
    print("2. BLIP Large (Salesforce/blip-image-captioning-large)")

    try:
        model_choice = int(input("Enter the number corresponding to your choice: "))
        if model_choice == 1:
            model_name = "Salesforce/blip-image-captioning-base"
            processor = BlipProcessor.from_pretrained(model_name)
            model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)
        elif model_choice == 2:
            model_name = "Salesforce/blip-image-captioning-large"
            processor = BlipProcessor.from_pretrained(model_name)
            model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)
        else:
            print("Invalid choice. Defaulting to BLIP Base.")
            model_name = "Salesforce/blip-image-captioning-base"
            processor = BlipProcessor.from_pretrained(model_name)
            model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)
    except ValueError:
        print("Invalid input. Defaulting to BLIP Base.")
        model_name = "Salesforce/blip-image-captioning-base"
        processor = BlipProcessor.from_pretrained(model_name)
        model = BlipForConditionalGeneration.from_pretrained(model_name).to(device)

    print(f"\nLoading BLIP model ({model_name})...")

    valid_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    files = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in valid_exts]

    if not files:
        print("\nNo images found to caption.\n")
        return

    print(f"\nGenerating captions in: {folder_path}")
    for img_file in files:
        txt_file = img_file.with_suffix(".txt")
        # Skip if .txt already exists
        if txt_file.exists():
            print(f"Skipping (already captioned): {txt_file.name}")
            continue

        image = Image.open(str(img_file)).convert("RGB")
        inputs = processor(image, return_tensors="pt").to(device)

        with torch.no_grad():
            out = model.generate(**inputs, max_length=30)
        caption = processor.decode(out[0], skip_special_tokens=True)

        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(caption + "\n")

        print(f"Captioned {img_file.name} -> {txt_file.name}: {caption}")

    print("\nCaptioning complete!")

    # Move images and captions to a new subfolder
    new_folder_name = f"{repeat_number}_{folder.name}"
    new_folder_path = folder / new_folder_name
    new_folder_path.mkdir(exist_ok=True)

    for file in files:
        txt_file = file.with_suffix(".txt")
        shutil.move(str(file), str(new_folder_path / file.name))
        if txt_file.exists():
            shutil.move(str(txt_file), str(new_folder_path / txt_file.name))

    print(f"\nFiles moved to: {new_folder_path}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python caption.py <folder_path>")
    else:
        caption_images_in_folder(sys.argv[1])
