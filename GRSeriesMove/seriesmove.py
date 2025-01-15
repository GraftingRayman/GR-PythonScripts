import os
import re
import shutil

def organize_files_by_title():
    # Regular expression to identify the title before "S0" or "S1" (case insensitive) and replace dots with spaces
    title_pattern = re.compile(r"^(.*?)(?=s[0123])", re.IGNORECASE)

    # Get the current working directory
    source_dir = os.getcwd()

    # Iterate through all files in the source directory
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            match = title_pattern.match(file_name)
            if match:
                # Extract the title and format it
                title = match.group(1).replace('.', ' ').strip()
                formatted_title = ' '.join(word.capitalize() for word in title.split())

                # Create the folder with the formatted title if it doesn't exist
                folder_path = os.path.join(source_dir, formatted_title)
                os.makedirs(folder_path, exist_ok=True)

                # Move the file into the folder
                destination_path = os.path.join(folder_path, file_name)
                shutil.move(file_path, destination_path)

    # Ensure all matching files are moved by processing all files again
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)

        if os.path.isdir(folder_path):
            for file_name in os.listdir(source_dir):
                file_path = os.path.join(source_dir, file_name)
                match = title_pattern.match(file_name)
                if os.path.isfile(file_path) and match:
                    title = match.group(1).replace('.', ' ').strip()
                    formatted_title = ' '.join(word.capitalize() for word in title.split())

                    if folder_name == formatted_title:
                        destination_path = os.path.join(folder_path, file_name)
                        shutil.move(file_path, destination_path)

if __name__ == "__main__":
    organize_files_by_title()
