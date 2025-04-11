import os
import sys
import requests
import json

# when update 
# first : git add update.py
# Second : git commit -m "Updated update.py"
# third : git push origin main

# File path to save the update status
update_file = "update_status.json"

# GitHub URL for the raw update file
url = "https://raw.githubusercontent.com/idkmanegtegeg/update-checker/main/update.py"


def get_current_version():
    """Check the current version from the selfbot."""
    if os.path.exists(update_file):
        with open(update_file, 'r') as file:
            data = json.load(file)
            return data.get("version", "1.0.0")
    return "1.0.0"  # Default if no update status file exists

def fetch_latest_version():
    """Fetch the latest version from GitHub."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extract version from the raw content
            version = response.text.split("version = '")[1].split("'")[0]
            return version
        else:
            print("Error: Unable to fetch the update.")
            return None
    except Exception as e:
        print(f"Error while fetching the update: {e}")
        return None


def update_selfbot():
    """Update the selfbot's code by replacing the existing update.py."""
    latest_version = fetch_latest_version()
    if latest_version:
        with open("selfbot.py", "w") as file:
            file.write(latest_version)
        print("Selfbot updated successfully!")
        return True
    return False

def check_for_update():
    """Check if the selfbot is running the latest version."""
    current_version = get_current_version()
    print(f"Current version: {current_version}")

    latest_version = fetch_latest_version()
    if latest_version:
        if latest_version != current_version:
            print("A new update is available!")
            if update_selfbot():
                print("Selfbot updated successfully!")
            else:
                print("Failed to update selfbot.")
        else:
            print("Selfbot is up to date.")
    else:
        print("Unable to check for updates.")

if __name__ == "__main__":
    check_for_update()
