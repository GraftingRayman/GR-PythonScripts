import os
import subprocess

def create_video_with_audio(output_filename="output.mp4", image_duration_1=21, image_duration_2=6):
    # Get all image and audio files in the current directory
    image_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff")
    audio_files = {"countdown.mp3": image_duration_1, "reveal.mp3": image_duration_2}

    image_files = sorted([f for f in os.listdir() if f.endswith(image_extensions)])
    if not image_files:
        print("No image files found in the current directory.")
        return

    if not all(audio in os.listdir() for audio in audio_files):
        print("Required audio files 'countdown.mp3' and 'reveal.mp3' are missing.")
        return

    print(f"Found {len(image_files)} images.")

    # Create directories for intermediate files
    segments_dir = "segments"
    combined_dir = "combined"
    os.makedirs(segments_dir, exist_ok=True)
    os.makedirs(combined_dir, exist_ok=True)

    # Process images in pairs: 1st image (countdown.mp3), 2nd image (reveal.mp3)
    combined_videos = []
    for i in range(0, len(image_files), 2):
        # Create video for 1st image with countdown.mp3
        segment_1 = create_video_segment(image_files[i], "countdown.mp3", image_duration_1, segments_dir)
        segment_2 = None

        # If there's a 2nd image, create video with reveal.mp3
        if i + 1 < len(image_files):
            segment_2 = create_video_segment(image_files[i + 1], "reveal.mp3", image_duration_2, segments_dir)

        # Combine the two segments into one video
        if segment_2:
            combined_segment = os.path.join(combined_dir, f"combined_{i // 2 + 1}.mp4")
            join_segments([segment_1, segment_2], combined_segment)
            combined_videos.append(combined_segment)
        else:
            # If there's no second image, just add the single segment
            combined_videos.append(segment_1)

    # Combine all combined videos into the final output
    join_segments(combined_videos, output_filename)

    print(f"Final video saved to: {output_filename}")

def create_video_segment(image_file, audio_file, duration, segments_dir):
    """Create a video segment from an image and an audio file."""
    segment_filename = f"segment_{os.path.splitext(image_file)[0]}.mp4"
    output_segment = os.path.join(segments_dir, segment_filename)
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-loop", "1",
                "-i", image_file,
                "-i", audio_file,
                "-c:v", "libx264",
                "-r", "30",  # Set frame rate to 30 FPS
                "-t", str(duration),
                "-pix_fmt", "yuv420p",
                "-shortest",
                output_segment
            ],
            check=True
        )
        print(f"Created segment: {output_segment}")
        return output_segment
    except subprocess.CalledProcessError as e:
        print(f"Error creating segment for {image_file} with {audio_file}:", e)
        return None

def join_segments(segments, output_file):
    """Join the segments into a single video."""
    join_list_file = "join_list.txt"
    try:
        with open(join_list_file, "w") as f:
            for segment in segments:
                f.write(f"file '{segment}'\n")

        subprocess.run(
            [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", join_list_file,
                "-c", "copy",
                output_file
            ],
            check=True
        )
        print(f"Joined video saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error joining segments:", e)
    finally:
        if os.path.exists(join_list_file):
            os.remove(join_list_file)

if __name__ == "__main__":
    create_video_with_audio(output_filename="final_output.mp4")
