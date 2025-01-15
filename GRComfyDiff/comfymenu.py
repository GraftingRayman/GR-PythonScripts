import requests
import os
import json
import sys
import threading
from datetime import datetime, timedelta
from jsondiff import diff
def get_user_input():
    print("\n=== ComfyDiff Checker ===")
    print("1. Compare two specific dates")
    print("2. Compare a specific date with the previous day")
    print("3. Download the latest file and check differences")
    print("4. Delete the latest file")
    print("5. Open the diff file with Notepad")
    print("6. Open the comfydiff folder")
    print("7. Exit")
    return input("Select an option: ").strip()
def get_date_input(prompt):
    while True:
        date_input = input(prompt).strip()
        try:
            return datetime.strptime(date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
class ComfyDiffChecker:
    def __init__(self, repo_url, folder_name="c:\\utils\\comfydiff", overwrite=True):
        self.repo_url = repo_url
        self.folder_name = folder_name
        self.overwrite = overwrite
        self.auto_executing = False
        os.makedirs(self.folder_name, exist_ok=True)
    def generate_filenames(self, date):
        return os.path.join(self.folder_name, f"custom-node-list-{date}.json")
    def get_commit_by_date(self, date):
        api_url = f"https://api.github.com/repos/ltdrdata/ComfyUI-Manager/commits"
        try:
            response = requests.get(api_url, params={"until": date, "per_page": 1})
            response.raise_for_status()
            commits = response.json()
            return commits[0]["sha"] if commits else None
        except requests.RequestException:
            return None
    def download_file(self, date, save_as):
        if os.path.exists(save_as):
            return
        commit_hash = self.get_commit_by_date(date)
        if not commit_hash:
            return
        file_url = f"https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/{commit_hash}/custom-node-list.json"
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            with open(save_as, 'w', encoding='utf-8') as file:
                file.write(response.text)
        except requests.RequestException:
            pass
    def download_latest_file(self):
        latest_date = datetime.now().strftime("%Y-%m-%d")
        latest_file = self.generate_filenames(latest_date)
        previous_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        previous_file = self.generate_filenames(previous_date)
        if not os.path.exists(latest_file):
            commit_hash = self.get_commit_by_date(latest_date)
            if not commit_hash:
                print("Unable to fetch the latest file commit.")
                return
            file_url = f"https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/{commit_hash}/custom-node-list.json"
            try:
                response = requests.get(file_url)
                response.raise_for_status()
                with open(latest_file, 'w', encoding='utf-8') as file:
                    file.write(response.text)
                print(f"Latest file saved: {latest_file}")
            except requests.RequestException as e:
                print(f"Failed to download the latest file: {e}")
                return
        if not os.path.exists(previous_file):
            print(f"Previous file not found: {previous_file}. Skipping comparison.")
            self.write_differences({}, append=False)
            return
        differences = self.calculate_differences(previous_file, latest_file)
        if differences:
            self.write_differences(differences, append=False)
        else:
            print("No differences detected.")
            self.write_differences({}, append=False)
    def delete_latest_file(self):
        latest_date = datetime.now().strftime("%Y-%m-%d")
        latest_file = self.generate_filenames(latest_date)
        if os.path.exists(latest_file):
            os.remove(latest_file)
    def open_diff_file(self):
        diff_file = os.path.join(self.folder_name, "comfydifference.txt")
        if os.path.exists(diff_file):
            os.system(f"notepad {diff_file}")
    def open_comfydiff_folder(self):
        os.system(f"explorer {self.folder_name}")
    def load_json_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    def calculate_differences(self, file1, file2):
        data1 = self.load_json_file(file1)
        data2 = self.load_json_file(file2)
        return diff(data1, data2, syntax='symmetric') if data1 and data2 else None
    def write_differences(self, differences, append=False):
        if self.auto_executing:
            return
        mode = 'w' if not append else 'a'
        difference_filename = os.path.join(self.folder_name, "comfydifference.txt")
        def stringify_keys(obj):
            if isinstance(obj, dict):
                return {str(key): stringify_keys(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [stringify_keys(item) for item in obj]
            else:
                return obj
        stringified_differences = stringify_keys(differences)
        with open(difference_filename, mode, encoding='utf-8') as diff_file:
            diff_file.write("\n=== ComfyDiff Differences ===\n")
            diff_file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            diff_file.write(json.dumps(stringified_differences, indent=4) if stringified_differences else "No differences found.\n")
    def auto_select(self):
        self.auto_executing = True
        self.delete_latest_file()
        self.download_latest_file()
        self.open_diff_file()
        sys.exit()
    def run(self):
        timer = threading.Timer(30.0, self.auto_select)
        timer.start()
        while True:
            choice = get_user_input()
            timer.cancel()
            if choice == '1':
                date1 = get_date_input("Enter the first date (YYYY-MM-DD): ")
                date2 = get_date_input("Enter the second date (YYYY-MM-DD): ")
                file1 = self.generate_filenames(date1)
                file2 = self.generate_filenames(date2)
                self.download_file(date1, file1)
                self.download_file(date2, file2)
                differences = self.calculate_differences(file1, file2)
                if differences:
                    self.write_differences(differences, append=False)
            elif choice == '2':
                date = get_date_input("Enter the date to compare (YYYY-MM-DD): ")
                previous_date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
                file1 = self.generate_filenames(previous_date)
                file2 = self.generate_filenames(date)
                self.download_file(previous_date, file1)
                self.download_file(date, file2)
                differences = self.calculate_differences(file1, file2)
                if differences:
                    self.write_differences(differences, append=False)
            elif choice == '3':
                self.download_latest_file()
            elif choice == '4':
                self.delete_latest_file()
            elif choice == '5':
                self.open_diff_file()
            elif choice == '6':
                self.open_comfydiff_folder()
            elif choice == '7':
                break
            timer = threading.Timer(30.0, self.auto_select)
            timer.start()
if __name__ == "__main__":
    repo_url = "https://github.com/ltdrdata/ComfyUI-Manager"
    checker = ComfyDiffChecker(repo_url, overwrite=True)
    checker.run()
