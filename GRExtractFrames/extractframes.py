import os
import sys
import subprocess

def extract_frames(video_file, output_format="jpg"):
    # Check if the file exists
    if not os.path.isfile(video_file):
        print(f"Error: File '{video_file}' does not exist.")
        return
    
    # Get the directory and base name of the file
    dir_name = os.path.dirname(video_file)
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    
    # Construct the output pattern
    output_pattern = os.path.join(dir_name, f"{base_name}_frame_%04d.{output_format}")
    
    # FFmpeg command
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", video_file,
        output_pattern
    ]
    
    # Run the FFmpeg command
    print(f"Extracting frames from '{video_file}'...")
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"Frames extracted to '{dir_name}' with pattern '{base_name}_frame_%04d.{output_format}'.")
    except subprocess.CalledProcessError:
        print("Error: Failed to extract frames. Make sure FFmpeg is installed and the video file is valid.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_frames.py <video_filename>")
    else:
        video_filename = sys.argv[1]
        # Change 'jpg' to 'png' if you want PNG files
        extract_frames(video_filename, output_format="jpg")
