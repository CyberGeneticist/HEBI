# Python 3.9.5
import json

import constants as c


def ensure_json_exists():
    try:
        # Open file in exclusive creation 'x' mode, which creates the file if it does not exist:
        with open(c.SAVE_FILE_PATH, "x") as save_file:
            # Write an empty JSON array to the newly created file - necessary for downstream JSON operations:
            json.dump([], save_file)
    # The above fails if the file already exists:
    except FileExistsError:
        pass

    try:
        # Try to decode JSON from the file in read 'r' mode:
        with open(c.SAVE_FILE_PATH, "r") as save_file:
            json.load(save_file)
    # If it fails because of incorrect JSON structure, write an empty JSON array to the file to fix it:
    except json.decoder.JSONDecodeError:
        with open(c.SAVE_FILE_PATH, "w") as save_file:
            json.dump([], save_file)


def load_saves():
    ensure_json_exists()
    
    with open(c.SAVE_FILE_PATH, "r") as save_file:
        saves = json.load(save_file)
    
    return saves


def save_saves(score, player_name):
    ensure_json_exists()

    # Read all the saves from file - a list of dictionaries:
    saves = load_saves()
    # Add the new player name - score dictionary into the list of saves:
    saves.append({"player_name": player_name, "score": score})

    # Finally, save the modified saves list:
    with open(c.SAVE_FILE_PATH, "w") as save_file:
        json.dump(saves, save_file)
