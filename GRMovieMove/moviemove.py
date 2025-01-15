import os
import re
import shutil

def move_folders_by_year():
    # Regular expression to match folder names containing a year in brackets, e.g., "Folder Name [2023]" or "Folder Name (2023)"
    year_pattern = re.compile(r"[\[(](\d{4})[\])]")

    # Get the current working directory
    source_dir = os.getcwd()

    # Iterate through all items in the source directory
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)

        # Check if it's a directory and matches the year pattern
        if os.path.isdir(folder_path):
            match = year_pattern.search(folder_name)
            if match:
                year = int(match.group(1))  # Extract the year as an integer

                # Determine the target directory based on the year
                if year < 1970:
                    year_dir = os.path.join(source_dir, "0 - 1969")
                else:
                    year_dir = os.path.join(source_dir, str(year))

                # Create the target directory if it doesn't exist
                os.makedirs(year_dir, exist_ok=True)

                # Move the folder into the target directory
                destination_path = os.path.join(year_dir, folder_name)
                shutil.move(folder_path, destination_path)

                print(f"Moved folder '{folder_name}' to '{year_dir}'")

if __name__ == "__main__":
    move_folders_by_year()
