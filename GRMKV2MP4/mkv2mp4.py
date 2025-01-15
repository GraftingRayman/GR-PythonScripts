import subprocess
import os

def convert_all_mkv_to_mp4(directory):
    """
    Converts all MKV files in the specified directory to MP4 format by copying the video and audio codecs.

    :param directory: Directory containing the MKV files.
    """
    ffmpeg_path = r"C:\utils\ffmpeg.exe"  # Path to ffmpeg.exe

    for file_name in os.listdir(directory):
        if file_name.endswith('.mkv'):
            input_file = os.path.join(directory, file_name)
            output_file = os.path.join(directory, file_name.replace('.mkv', '.mp4'))

            try:
                # Use ffmpeg to copy video and audio codecs without re-encoding
                command = [
                    ffmpeg_path,
                    '-i', input_file,
                    '-vcodec', 'copy',
                    '-acodec', 'copy',
                    output_file
                ]
                subprocess.run(command, check=True)
                print(f"Converted: {file_name} -> {file_name.replace('.mkv', '.mp4')}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {file_name}:", e)

# Run the conversion in the current directory
current_directory = os.getcwd()
convert_all_mkv_to_mp4(current_directory)
