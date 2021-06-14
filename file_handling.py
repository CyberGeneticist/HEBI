# Python 3.9.5
import json

import constants as c


def ensure_json_exists(file_path, top_level):
    if top_level.lower() in ("array", "list"):
        top_level = []
    elif top_level.lower() in ("object", "dictionary"):
        top_level = {}
    else:
        raise ValueError("The 'top_level_object' argument passed to 'ensure_json_exists' must be either an 'array' or 'object' string.")

    try:
        # Open file in exclusive creation 'x' mode, which creates the file if it does not exist:
        with open(file_path, "x") as save_file:
            # Write an empty JSON array to the newly created file - necessary for downstream JSON operations:
            json.dump(top_level, save_file)
    # The above fails if the file already exists:
    except FileExistsError:
        pass

    try:
        # Try to decode JSON from the file in read 'r' mode:
        with open(file_path, "r") as save_file:
            json.load(save_file)
    # If it fails because of incorrect JSON structure, write an empty JSON array to the file to fix it:
    except json.decoder.JSONDecodeError:
        with open(file_path, "w") as save_file:
            json.dump(top_level, save_file)


def load_saves():
    ensure_json_exists(c.SAVE_FILE_PATH, "array")
    
    with open(c.SAVE_FILE_PATH, "r") as save_file:
        saves = json.load(save_file)
    
    return saves


def save_saves(score, player_name):
    ensure_json_exists(c.SAVE_FILE_PATH, "array")

    # Read all the saves from file - a list of dictionaries:
    saves = load_saves()
    # Add the new player name - score dictionary into the list of saves:
    saves.append({"player_name": player_name, "score": score})

    # Finally, save the modified saves list:
    with open(c.SAVE_FILE_PATH, "w") as save_file:
        json.dump(saves, save_file)


def save_settings(**kwargs):
    ensure_json_exists(c.SETTINGS_FILE_PATH, "object")

    with open(c.SETTINGS_FILE_PATH, "w") as settings_file:
        json.dump(kwargs, settings_file)


def load_settings():
    ensure_json_exists(c.SETTINGS_FILE_PATH, "object")

    with open(c.SETTINGS_FILE_PATH, "r") as settings_file:
        settings = json.load(settings_file)

    return settings
