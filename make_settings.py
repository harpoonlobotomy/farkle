"""just a quick script to make a new settings file in a given directory."""


settings_dict = {
    "defaults": {
        "player1_name": "player_1",
        "player1_col": "#5AC280",
        "player2_name": "player_2",
        "player2_col": "#5A90C2",
        "playstyle": "harpoon",
        "is_singleplayer": True,
        "computer_think_aloud": False,
        "game_theme": "arcade",
        "output_file": "farkle_output.json"
    },
    "user_set": {
    }
}

def make_settings_file():
    import json
    import os

    print(f"[CREATING NEW SETTINGS FILE]\n\n A new settings file will be created in: `{os.getcwd()}`)")
    """while True:
        dir_input = input("Directory: ")
        if dir_input:
            dir_path = os.path.abspath(dir_input)
            if not os.path.exists(dir_path):
                print(f"Directory `{dir_path}` does not exist. Please create it or enter a different directory.")
            else:
                break
        else:
            dir_path = os.getcwd()
            break"""

    with open(os.path.join(os.getcwd(), "farkle_settings.json"), "w") as f:
        json.dump(settings_dict, f, indent=4)

    print("Settings file created successfully at `{}`".format(os.path.join(os.getcwd(), "farkle_settings.json"))) # why use .format instead of putting in an fstring?
    return os.path.join(os.getcwd(), "farkle_settings.json")

def check_settings_file():
    import os
    import json

    settings_path = os.path.join(os.getcwd(), "farkle_settings.json")
    if not os.path.exists(settings_path):
        print("No settings file found in current directory. Creating new settings file...")
        settings_path = make_settings_file()
    else:
        print("Settings file found at `{}`. Loading settings...".format(settings_path))

    with open(settings_path, "r") as f:
        settings_file_dict = json.load(f)

    found_missing = False
    for key in settings_dict["defaults"]:
        if key not in settings_file_dict["defaults"]:
            print(f"ERROR: KEY {key} NOT FOUND IN SETTINGS FILE. PLEASE CHECK YOUR SETTINGS FILE AND MAKE SURE IT CONTAINS ALL NECESSARY KEYS.\nTHIS SHOULD NEVER HAPPER.\n")
            input("Press enter to continue...")
            found_missing = True
            settings_file_dict["defaults"][key] = settings_dict["defaults"][key] # shouldn't be necessary, but to protect against incorrectly generated settings files?

    if found_missing:
        print("Missing keys have been added to settings file with default values. Please check your settings file and make sure it contains all necessary keys.")
        with open(settings_path, "w") as f:
            json.dump(settings_file_dict, f, indent=4)
        input("Press enter to continue...")
    return settings_file_dict
