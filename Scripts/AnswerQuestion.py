import json
import os
import sys

def run():

    if len(sys.argv) <= 1:
        print("You need to supply a colour")
        exit()

    #Params from our arguments
    username = sys.argv[1].strip()
    choice = sys.argv[2].strip().upper()
    pointString = sys.argv[3].strip()

    #validation
    if not username:
        return "I cant work out your username and I don't know how, bad bot!"

    possibleAnswers = ["A", "B", "C", "D", "TRUE", "FALSE"]
    if not choice in (answer.upper() for answer in possibleAnswers):
        seperator = ", "
        return f"@{username} you must use one of the following answers: {possibleAnswers}".format(seperator.join(possibleAnswers))

    if not pointString.isdigit():
        return f"@{username} you have to bet a number pal"
    
    points = int(pointString)
    if points < 10 or points > 10000:
        return f"@{username} you must bet between 10 and 10,000 points"

    filename = r"D:/Projects/Twitch/Html/Quiz/data.json"

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
    return f"@{username} chose {choice} for {points} points"

print(run())