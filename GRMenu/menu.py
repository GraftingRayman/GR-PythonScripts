import os
import subprocess
import sys

def list_files_by_extension(folder_path, extension):
    """List all files with the given extension in the specified folder, skipping certain files."""
    return [f for f in os.listdir(folder_path) if f.endswith(extension) and "- Copy" not in f and f not in ["menu.bat", "menu.py"]]

def display_menu(python_scripts, batch_files):
    """Display a menu of Python scripts and batch files side by side."""
    print("\nAvailable Files:")
    print(f"{'Python Scripts':<40}\tBatch Files")
    max_len = max(len(python_scripts), len(batch_files))
    for i in range(max_len):
        py_entry = f"{i + 1}. {python_scripts[i]}" if i < len(python_scripts) else ""
        batch_entry = f"{chr(97 + i).upper()}. {batch_files[i]}" if i < len(batch_files) else ""
        print(f"{py_entry:<40}\t{batch_entry}")
    print("\n0. Exit")

def main():
    folder_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please try again.")
        return

    while True:
        python_scripts = list_files_by_extension(folder_path, ".py")
        batch_files = list_files_by_extension(folder_path, ".bat")

        if not python_scripts and not batch_files:
            print("No Python or batch files found in the specified folder.")
            break

        display_menu(python_scripts, batch_files)

        try:
            user_input = input("Enter the number/letter of the file to run followed by any parameters (e.g., '14 c:\\utils') or 0 to exit: ").strip()

            if user_input == "0":
                print("Exiting the menu.")
                break

            if user_input.isdigit():
                choice = int(user_input)
                if 1 <= choice <= len(python_scripts):
                    script_to_run = os.path.join(folder_path, python_scripts[choice - 1])
                    params = input("Enter parameters for the script (or press Enter to skip): ").strip().split()
                    print(f"\nRunning Python script: {python_scripts[choice - 1]} with parameters: {' '.join(params)}\n")
                    subprocess.run(["python", script_to_run, *params], check=True)
                else:
                    print("Invalid choice for Python scripts. Please try again.")
            elif user_input.isalpha() and len(user_input) == 1:
                choice = ord(user_input.lower()) - 97  # Convert letter to index (a=0, b=1, etc.)
                if 0 <= choice < len(batch_files):
                    batch_to_run = os.path.join(folder_path, batch_files[choice])
                    params = input("Enter parameters for the batch file (or press Enter to skip): ").strip()
                    print(f"\nRunning batch file: {batch_files[choice]} with parameters: {params}\n")
                    subprocess.run([batch_to_run, *params.split()], shell=True, check=True)
                else:
                    print("Invalid choice for batch files. Please try again.")
            else:
                print("Invalid input. Please enter a valid number or letter.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
