import cv2
import os
import numpy as np
from pathlib import Path

def convert_to_pencil_sketch(image_path, output_dir):
    """
    Convert an image to pencil sketch style
    """
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Could not read image: {image_path}")
            return
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Invert the grayscale image
        inverted = 255 - gray
        
        # Apply Gaussian blur to the inverted image
        # You can adjust the kernel size (e.g., (21, 21)) for different effects
        blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
        
        # Invert the blurred image back
        inverted_blur = 255 - blurred
        
        # Create the pencil sketch by blending
        sketch = cv2.divide(gray, inverted_blur, scale=256.0)
        
        # Get the original filename and create output path
        original_filename = Path(image_path).stem
        output_filename = f"{original_filename}_sketch.png"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save the sketch image
        cv2.imwrite(output_path, sketch)
        print(f"Saved: {output_path}")
        
        return sketch
        
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")

def process_directory(input_dir=".", output_dir="sketches"):
    """
    Process all images in the directory
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    
    # Get all image files in the current directory
    files = [f for f in os.listdir(input_dir) 
             if os.path.isfile(os.path.join(input_dir, f)) and 
             Path(f).suffix.lower() in image_extensions]
    
    if not files:
        print(f"No image files found in {input_dir}")
        return
    
    print(f"Found {len(files)} image(s) to process...")
    
    # Process each image
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        print(f"Processing: {filename}")
        convert_to_pencil_sketch(input_path, output_dir)
    
    print(f"\nAll images processed! Sketches saved in '{output_dir}' folder.")

def show_preview(image_path):
    """
    Show a before/after preview (optional)
    """
    try:
        # Load original image
        original = cv2.imread(image_path)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        
        # Create sketch
        sketch = convert_to_pencil_sketch(image_path, "temp_preview")
        
        if sketch is not None:
            # Display images (if you want to see them)
            import matplotlib.pyplot as plt
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            
            ax1.imshow(original)
            ax1.set_title("Original Image")
            ax1.axis('off')
            
            ax2.imshow(sketch, cmap='gray')
            ax2.set_title("Pencil Sketch")
            ax2.axis('off')
            
            plt.tight_layout()
            plt.show()
            
            # Clean up temp file
            temp_file = os.path.join("temp_preview", f"{Path(image_path).stem}_sketch.png")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists("temp_preview") and not os.listdir("temp_preview"):
                os.rmdir("temp_preview")
                
    except ImportError:
        print("matplotlib not installed. Install it with: pip install matplotlib")
    except Exception as e:
        print(f"Could not display preview: {str(e)}")

if __name__ == "__main__":
    import sys
    
    # Process command line arguments
    preview = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "--preview" and len(sys.argv) > 2:
            # Preview a specific image
            if os.path.exists(sys.argv[2]):
                show_preview(sys.argv[2])
                sys.exit(0)
            else:
                print(f"File not found: {sys.argv[2]}")
        elif sys.argv[1] == "--preview":
            print("Please specify an image file to preview")
            print("Usage: python script.py --preview image.jpg")
            sys.exit(1)
    
    # Process all images in current directory
    process_directory()