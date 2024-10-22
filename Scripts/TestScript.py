import json
import os

def run():

    filename = "D:\My Documents\My Videos\Projects\Twitch\Html\Quiz\data.json"

    choice = "C"
    points = 500
    username = "Joeborder_123"

    new_entry = {
        "Username": username,
        "Points": points,
        "Choice": choice
    }

    if os.path.exists(filename):
        # File exists, read the existing data
        with open(filename, 'r') as f:
            try:
                data = json.load(f)  # Load existing data as JSON
            except json.JSONDecodeError:
                data = []  # If file is empty or corrupted, start fresh
    else:
        # File doesn't exist, create an empty list
        data = []


    updated_data = [obj for obj in data if obj.get('Username') != username]
    updated_data.append(new_entry)

    with open(filename, 'w') as f:
        json.dump(updated_data, f, indent=4)

    # Return any data here that you'd like to use
    return updated_data

print(run())