"""simple text-based farkle game
started April 2026 //  [gui version] v 1.7 // harpoonlobotomy"""

# Command to build a .exe file:
#   [cd to py file dir first] pyinstaller --onefile --noupx --icon farkle_gui.ico farkle_gui.pyw

# have commented out to_json throughout, add it back later.
from time import sleep
import random, os
import FreeSimpleGUI as sg
from PIL import Image#, ImageSequence, ImageTk

die_refresh_val = 0.135
points_to_win = 4000

canvas_col = None#"white"
region_1_col = None#"red"
region_2_col = None#"magenta"
region_3_col = None#"blue"

no_to_farkle = {
    "die_1": "f",
    "die_2": "a",
    "die_3": "r",
    "die_4": "k",
    "die_5": "l",
    "die_6": "e"
}
farkle_to_no = {
    "f": "die_1",
    "a": "die_2",
    "r": "die_3",
    "k": "die_4",
    "l": "die_5",
    "e": "die_6"
}

no_to_bust = {
    "die_1": "d", ## d for 'dash' so make_other works properly
    "die_2": "b",
    "die_3": "u",
    "die_4": "s",
    "die_5": "t",
    "die_6": "d"
}

window_is_closed = False

class settings:

    player1_name:str = None
    player1_col:str = None
    player2_name:str = None
    player2_col:str = None

    player_roll_speed:float = 0.2
    computer_roll_speed:float = 0.2
    playstyle:str = None
    is_singleplayer:bool = None
    computer_think_aloud:bool = None
    output_file:str = None
    game_theme:str = None

    roll_on_start:bool = False
    export_to_file:bool = False

    t:theme_data = None

    def init(self, settings_dict):

        for item in settings_dict["defaults"]: # counted here as long as the type is given, apparently. Can't be the best way to do this but seems to be working so will go with it.

            setattr(settings, item, settings_dict["user_set"][item] if settings_dict["user_set"].get(item) else settings_dict["defaults"][item])

        self.player_roll_speed = self.player_roll_speed / 1000
        self.computer_roll_speed = self.computer_roll_speed / 1000

class theme_data():

    def __init__(self):
        pass

    eggplant = "#3E2857",
    navy = "#284157"
    ivory = "#E0DAC5"

    theme_dict:dict = {
        "farkle_navy": {'BACKGROUND': navy,
                    'TEXT': "#B08F23",
                    'INPUT': "#45523F",
                    'TEXT_INPUT': "#f5db74",
                    'SCROLL': "#003e9b",
                    'BUTTON': ('black', "#F8DC5E"),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 3,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0,
                    'dot_colour': "#B08F23",
                    'font': "courier 14 bold",
                    "alt_tally_bg": "#332b26",
                    "title_bg": navy,
                    "gold_text": "#ffd768",
                    'button_mouseover': ("#ecd341", "#2d1f11")
                    },

        "farkle_tan": {'BACKGROUND': ivory,
                    'TEXT': "#25775f",
                    'INPUT': "#45523F",
                    'TEXT_INPUT': "#f5db74",
                    'SCROLL': "#003e9b",
                    'BUTTON': ('black', "#F8DC5E"),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 3,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0,
                    'dot_colour': "#332b26",
                    'font': "courier 14 bold",
                    "alt_tally_bg": "#CDC9A6",
                    "title_bg": ivory,
                    "gold_text": "#442D15",
                    "button_mouseover": ("#CDC9A6", "#25775f")
                    },

        "farkle_arcade": {'BACKGROUND': "#38354a",
                    'TEXT': "#de4507",
                    'INPUT': "#45523F",
                    'TEXT_INPUT': "#f5db74",
                    'SCROLL': "#003e9b",
                    'BUTTON': ('black', "#ffda57"),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 3,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0,
                    'dot_colour': "#d35700",
                    'font': "courier 14 bold",
                    "alt_tally_bg": "#433e5e",
                    "title_bg": "#382b43",
                    "gold_text": "#f0c762",
                    'ACCENT1': '#FF0266','ACCENT2': '#FF5C93','ACCENT3': '#C5003C',
                    'button_mouseover':("#ecd341", "#431c4a")
                    }}

    def init_themes(self):

        sg.theme_add_new('farkle_tan', self.theme_dict["farkle_tan"])
        sg.theme_add_new('farkle_navy', self.theme_dict["farkle_navy"])
        sg.theme_add_new('farkle_arcade', self.theme_dict["farkle_arcade"])

def init_settings():

    def check_for_settings_file():
        # shorter than it used to be, no longer allows for user input of settings directory. Would like to add that back in but don't know how at present.
        from make_settings import check_settings_file
        settings_dict = check_settings_file()
        return settings_dict

    settings_dict = check_for_settings_file()
    settings.init(settings, settings_dict)

    theme_name = settings_dict["user_set"]["game_theme"] if settings_dict["user_set"].get("game_theme") else settings_dict["defaults"]["game_theme"]
    if "farkle_" in theme_name:
        theme_name = theme_name.replace("farkle_", "")
    t = theme_data()
    settings.t=t
    t.init_themes()
    sg.theme(f'farkle_{theme_name}')

gold = "#ffff7f" # "gold"
std_dot_size=10
widest_measure = 340#560#340
std_btn = 10

button_held = "#F8DC5E"
button_used = "#666354"

die_bust_col = ('white', "#330303")

point_value = ''
output_line_str = ''

SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'

bust_text = {
    "die_1": "d",
    "die_2": "b",
    "die_3": "u",
    "die_4": "s",
    "die_5": "t",
    "die_6": "d",
}

tally_text_col = None

png_icon = "farkle_icon_48.png"


class print_colours:

    def __init__(self):
        self.default:str = "white"
        self.input:str = "cyan"
        self.output:str = "nobold_cyan"
        self.points:str = "nobold_green"
        self.prompt:str = "white"
        self.pre_diceroll:str = "magenta"
        self.held_dice:str = "green"
        self.used_dice:str = "yellow"

    def playernm(self, player:"playerInst", format=None):

        end = colours[self.default]
        if player.skin:
            col = colours[player.skin] if colours.get(player.skin) else player.skin # else assume already a code, though I don't think it ever will be
        if format:
            end = getattr(self, format)
            if end:
                end = colours[end]
        return f"{col}{player.name}{end}"


print_colour = print_colours()

class pos_data:
    """dice_line / prompt_line / input_line / output_line"""
    def __init__(self, error, points, dice, prompt, inputstr, output):
        self.error_line:str = error
        self.points_line:str = points
        self.dice_line:str = dice
        self.prompt_line:str = prompt
        self.input_line:str = inputstr
        self.output_line:str = output
        self.clearline = "\033[0K"

        import shutil
        size = shutil.get_terminal_size()
        self.lines = size.lines - 2
        self.columns = size.columns

        self.tally = str(int((str(self.output_line).split("[")[1].split(";")[0])) + 3)
        self.tally_orig = int(self.tally) + 5
        self.dice_pos:dict[int, int] = {} # place_number: position in string

        last_pos = 0

        centred_dice = int((self.columns - len(positions))/2)-1
        centred_dice = (" " * centred_dice) + positions + (" " * centred_dice)

        for i in range(1, 7):
            last_pos = centred_dice.find(str("["), last_pos + 1)
            self.dice_pos.setdefault(i, last_pos)

        self.pos:dict = dict()

    def __repr__(self):
        return (f"{self.dice_line}: dice // {self.prompt_line}: prompt // {self.input_line}: inputstr // {self.output_line}: output")

    def get_visible_length(self, text):
        # Regex to match ANSI escape codes

        #print(f"Visible length before: {len(text)}")
        import re
        for m in re.finditer(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', text):
            text = text.replace(m.group(0), '')
        #print(f"Visible length  after: {len(text)}")
        return len(text)

    def print_error(self, text, val=None):
        extra = ''
        if val:
            for _ in range(int(val)):
                extra=extra.join("\n")

        text = self.error_line + extra + text + self.clearline + END
        print(text, end='')


    def print_points(self, text, delay = False):

        if "\n" in text:
            text_parts = text.split("\n")
            #self.print_error(f"text parts: {str(text_parts)}", 3)

            for i, part in enumerate(text_parts):
                part_length = self.get_visible_length(part)
                centred_text = int((self.columns - part_length)/2)-1
                centred_text = (" " * centred_text) + part + (" " * centred_text)
                text = self.points_line + ("\n" * i) + centred_text + self.clearline + END # will break visually if too many newlines in a string, but works well for single line breaks.
                print(text, end = '')
                if delay:
                    sleep(.02)

        else:
            text_length = self.get_visible_length(text)
            centred_text = int((self.columns - text_length)/2)-1
            centred_text = (" " * centred_text) + text + (" " * centred_text)
            text = self.points_line + centred_text + self.clearline + END
            print(text, end = '')


    def print_dice(self, text='', die=None, skin=''):

        skin = colours[skin] if colours.get(skin) else skin
        if die:
            temp = self.dice_line.replace("7f", f"{self.dice_pos.get(die.place_no)+1}f")

        if isinstance(text, list):
            text = ''.join(text)

        if die:
            text = temp + skin + text + END
        else:
            text = self.dice_line + text
        print(text, end = '')

    def print_prompt(self, text=" ", clear=False):

        if clear:
            text = print(self.prompt_line, self.clearline, end='')
            return
        centred_text = int((self.columns - len(text))/2)-1
        centred_text = (" " * centred_text) + text + (" " * centred_text)
        text = self.prompt_line + centred_text + self.clearline + END
        print(text, end = '')


    def print_input(self, text):

        centred_text = int((self.columns - len(text))/2)-1
        centred_text = (" " * (centred_text - 12)) + text
        text = self.input_line + colours[print_colour.input] + centred_text + self.clearline + END
        print(text, end = '')


    def print_output(self, text, clear=False):

        store_text = ''
        if clear:
            text = print(self.output_line, self.clearline, end='')
            return
        print(f"{self.output_line}{self.clearline}")
        if "[[" in text:
            store_text = text
            text = text.replace("[[", "").replace("]]", "").strip()

        text_length = self.get_visible_length(text) + len("[    ]")
        centred_text = int((self.columns - text_length)/2)-1#len(f"[  {text}  ]"))/2)-1
        if store_text:
            import re
            for m in re.finditer(r"\[\[(\w+)]]", store_text):
                text = "\033[2;32m" + m.group(1) + colours[print_colour.output]
                store_text = store_text.replace(m.group(0), text)
                text = store_text

        centred_text = (" " * centred_text) + "[  " + text + "  ]"
        text = self.output_line + colours[print_colour.output] + centred_text + END
        print(text, end='')
        #print(self.clearline, end='')


class dice_gifs:
    """ num_by_colour includes every number to every number, and every other char to blank (and inverse.)"""
    def __init__(self):
        self.keys = ["blank", "1", "2", "3", "4", "5", "6", "f", "a", "r", "k", "l", "e", "d", "b", "u", "s", "t"]
        self.player_1_path:str = ""
        #self.player_1_gifs:dict = {}#{{i:""} for i in keys} # each inner dict is {die_val: filepath} // from_x_to_y is always outgoing>incoming, and always stored on the x.
        self.player_1_stills:dict = {}
        self.player_2_path:str = ""
        #self.player_2_gifs:dict = {} # are these filepaths or Image.Image? Probably the former.
        self.player_2_stills:dict = {}
        self.farkle_bust_gifs:dict = {}
        self.farkle_stills:dict = {}
        #self.gif_frames = {} # filename > list of frames. Seems excessively wasteful and bad for memory. But idk what else to do about actually playing the damn gifs.
        self.held_still:dict[str:str] = {} # 1: held_1_filepath == dice_graphics\BASE\die_states
        self.used_still:dict[str:str] = {} # 1: used_1_filepath

gif_data = dice_gifs()

def get_farkle_gifs():
    self_roll_dir = f"{os.getcwd()}\\dice_graphics\\BASE\\self_roll\\"
    if not os.path.isdir(self_roll_dir):
        from make_dice_images import make_combination_image
        for letter in "farklebustd":
            make_combination_image(make_farkle = False, make_bust=False, make_other=[letter, letter], make_other_colour = None, other_subfolder="BASE\\self_roll", end_blank=False, filename=f"full_roll_{letter}", anim_frames=None)
    full_roll_paths = os.listdir(self_roll_dir)

    stills_dir = f"{os.getcwd()}\\dice_graphics\\BASE\\stills\\"
    if not os.path.isdir(stills_dir):
        from make_dice_images import make_single_frames
        make_single_frames(to_make="farklebustd", output_dir=stills_dir)
    stills = os.listdir(stills_dir)

    for letter in "farkledbustd":
        if full_roll_paths:
            results = list(f"{self_roll_dir}{i}" for i in full_roll_paths if f"roll_{letter}" in i) # only pure farkle letters here. Anything that mixes with player colours is in the player dict.
            if results:
                gif_data.farkle_bust_gifs[letter] = results[0]
        still_images = list(f"{stills_dir}{i}" for i in stills if i == f"{letter}.png")
        if still_images:
            gif_data.farkle_stills[letter] = still_images[0]

    die_states_dir = f"{os.getcwd()}\\dice_graphics\\BASE\\die_states\\"
    if not os.path.isdir(die_states_dir):
        print("Need to make die states stills")
        from make_dice_images import make_single_frames
        make_single_frames(to_make="123456", set_colour="used_die", output_dir=die_states_dir)
        print(f"Made used_die, now making held_die: {os.listdir(die_states_dir)}")

        make_single_frames(to_make="123456", set_colour="held_die", output_dir=die_states_dir)
        print(f"held_die made too: {os.listdir(die_states_dir)}")



    for file in os.listdir(f"{os.getcwd()}\\dice_graphics\\BASE\\die_states\\"):
        val = file[:1]
        if "held" in file:
            gif_data.held_still[val] = f"{os.getcwd()}\\dice_graphics\\BASE\\die_states\\" + file
        else:
            gif_data.used_still[val] = f"{os.getcwd()}\\dice_graphics\\BASE\\die_states\\" + file

def colour_dice_sets():

    """ Use PIL to colour the dice according to player colours."""
    for player in (players.player_1, players.player_2):
        player_dice_path = f"{os.getcwd()}\\dice_graphics\\num_by_colour\\{player.skin}\\"
        if not os.path.isdir(player_dice_path) or len(os.listdir(player_dice_path)) < 80: # arbitrarily 80 for now to catch anything obviously lacking.
            print(f"Generating dice images for {player}")
            from make_dice_images import colour_players_dice
            colour_players_dice(player_colour=player.skin, force_recolour=True, just_stills=True)

    gif_data.player_1_path = f"{os.getcwd()}\\dice_graphics\\num_by_colour\\{players.player_1.skin}\\"
    for key in gif_data.keys:
        #results = list(f"{gif_data.player_1_path}{i}" for i in os.listdir(gif_data.player_1_path) if i.split("_to_")[0] == key and ".gif" in i)
        #gif_data.player_1_gifs[key] = results
        still = list(f"{gif_data.player_1_path}{i}" for i in os.listdir(gif_data.player_1_path) if i == f"{key}.png")
        if still:
            gif_data.player_1_stills[key] = still[0]

    gif_data.player_2_path = f"{os.getcwd()}\\dice_graphics\\num_by_colour\\{players.player_2.skin}\\"
    for key in gif_data.keys:
        #results = list(f"{gif_data.player_2_path}{i}" for i in os.listdir(gif_data.player_2_path) if i.split("_to_")[0] == key  and ".gif" in i) #<<< this used to say 'player_1_path', but the correct colour roll was used. Check how - am I not using this and getting it elsewhere instead?
        #gif_data.player_2_gifs[key] = results
        still = list(f"{gif_data.player_2_path}{i}" for i in os.listdir(gif_data.player_2_path) if i == f"{key}.png")
        if still:
            gif_data.player_2_stills[key] = still

    get_farkle_gifs()

class die:
    def __init__(self, place_number = 1, skin=None):
        self.value = 9
        self.place_no = place_number
        self.held = False
        self.used = False
        self.skin = skin
        self.held_previously = False

    def __repr__(self):
        return f"<place_no: {self.place_no} / value: {self.value} / used: {self.used} / held: {self.held}>"

class dice_data:

    def __init__(self):

        self.skin = None
        self.dice:list[die] = list()
        self.by_no:dict[int, die] = {}
        """player_no[die_no] = {'still': bytes, 'anim': bytes}"""
        self.force_dicerolls = False
        self.showing_farkle = False

    def init_dice(self):

        if self.dice:
            self.dice = []

        for i in range(1, 7):
            die_inst = die(place_number=i, skin=self.skin)
            self.dice.append(die_inst)
            self.by_no[i] = die_inst

    def get_die_inst(self, key:str|int) -> die:
        if isinstance(key, str):
            key = key.replace("die_", "")
        die_inst = self.by_no[int(key)]
        return die_inst

    def hold(self, die_inst): # selecting by place_no; if there was a graphic, they would scatter to roll then scoot back to their positions.

        if die_inst.held:
            die_inst.held = False
        else:
            die_inst.held = True

        return die_inst

dice = dice_data()
dice.init_dice()

##### MAIN GAME ######

positions = "[  1  ]      [  2  ]      [  3  ]      [  4  ]      [  5  ]      [  6  ]"
END = "\033[0m"
HIDE = "\033[?25l"
SHOW = "\033[?25h"

colours = {
    "white": "\033[0;37m", # not bold because it's too bright otherwise.
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "nobold_green": "\033[0;32m",
    "yellow": "\033[1;33m",
    "blue": "\033[1;34m",
    "magenta": "\033[1;35m",
    "nobold_cyan": "\033[0;36m",
    "cyan": "\033[1;36m",
}

class outputter:

    def __init__(self):
        from uuid import uuid4
        self.session_ID:str = str(uuid4())[-6:]
        self.turn_data = {}
        self.game_data = {}

    def file_select(self, file_selection):

        if file_selection == "gamedata":
            file = settings.output_file

        elif file_selection == "settings":
            file = f"{os.getcwd()}\\farkle_settings.json"
        return file

    def load_json(self, file_selection):

        file = self.file_select(file_selection)
        if os.path.isfile(file):
            import json
            with open(file, "r") as f:
                file_data = json.load(f)
        else:
            file_data = {}

        return file_data

    def output_to_file(self, data, file_selection):

        file = self.file_select(file_selection)
        import json
        with open(file, "w") as f:
            json.dump(data, f, indent=2)


    def start_game(self):
        if not self.game_data:
            self.game_data = {self.session_ID: {0: {}}}
            print(f"Starting game: {self.game_data}")
        else:
            print("Game data already exists, not resetting.")


    def output_gamedata(self, end_game=False):

        if not settings.export_to_file:
            print("Not set to export to file.")
            return

        farkle_file = self.load_json("gamedata")

        gamedata = self.game_data.copy()

        if farkle_file:
            for entry in farkle_file:
                if entry and entry != self.session_ID:
                    gamedata[entry] = farkle_file[entry]

        if end_game:
            gamedata[self.session_ID][players.total_games]["game_score"] = {players.current.name: players.current.game_score, players.opponent.name: players.opponent.game_score}

        self.output_to_file(gamedata, "gamedata")

    def format_dicerolls(self):

        if not self.turn_data.get(players.total_turns):
            self.turn_data[players.total_turns] = {"player": players.current.name, "rolls": {}}

        current_data = self.turn_data[players.total_turns]
        current_data["rolls"][players.current.roll_count] = ({"Dice": list(f"{i.value}" if not i.used else f"{i.value} - USED" for i in dice.dice)}) # only excludes used dice, allows for any that /could/ potentially be selected instead of just those that are.

    def collect_turndata(self, matches=None, dice_rolled=None, roll_score=0, bust=False, turn_end=None, game_end=False):

        #print(f"Collecting turndata: \nMatches: {matches} // die_rolled: {dice_rolled} // roll_score: {roll_score} // bust: {bust} // turn_end: {turn_end} // game_end: {game_end} // initial_roll: {initial_roll}\n")
        """
            {total_turns}: {
                player: {player.name},
                rolls: [{matches}]
                turn_end_score: {turn_score: game_score}
            }

        """
        #write_turn_data = False#True
        #force_no_writing = True
        if not settings.export_to_file:#force_no_writing:
            print("not settings.export_to_file")
            return

        if dice_rolled:
            if not isinstance(dice_rolled, list):
                dice_rolled = list(dice_rolled)

        #if initial_roll:
            #initial_roll = list(i.value for i in dice.dice)

        if self.turn_data and self.turn_data.get(players.total_turns):
            current_data = self.turn_data[players.total_turns]
        else:
            #self.turn_data[players.total_turns] = {"player": players.current.name, "initial roll": initial_roll, "rolls": {}}
            self.turn_data[players.total_turns] = {"player": players.current.name, "rolls": {}} # no need for initial_roll if we get the rolls directly from roll_dice
            current_data = self.turn_data[players.total_turns]

        if matches:
            current_data["rolls"][players.current.roll_count].update({"Dice taken": matches, "Roll score": roll_score})

        if bust:
            current_data["rolls"][players.current.roll_count].update({"Dice taken": "BUST", "Roll score": roll_score})

        write_turn_data = True
        if turn_end:
            current_data["rolls"][players.current.roll_count].update({"Ending turn": players.current.turn_score if not bust else 0})
            current_data["game_score"] = players.current.game_score
            if write_turn_data:
                self.output_gamedata()

        self.game_data.setdefault(self.session_ID, {}).setdefault(players.total_games, {}).setdefault(players.total_turns, current_data)

        if game_end:
            self.output_gamedata(end_game=True)

to_json = outputter()

def remove_player_colour_gifs(keep_current=True):
    """ Currently only accessed via restore_defaults; should make it an option on its own. """

    import shutil

    if keep_current:
        to_keep = (players.player_1.skin, players.player_2.skin)
    else:
        to_keep = None

    directory = f"{os.getcwd()}\\dice_graphics\\num_by_colour\\"
    folders = os.listdir(directory)
    print(f"folders: {folders}")
    for folder in folders:
        if to_keep and folder in to_keep:
            continue
        print(f"Folder to remove: {directory}{folder}")
        shutil.rmtree(directory + folder)

def restore_defaults():

    settings_dict = to_json.load_json("settings")

    for item in settings_dict["defaults"]:
        #print(f"item in default dict: {settings_dict['defaults'][item]} // item: {item}")
        setattr(settings, item, settings_dict["defaults"][item])

    theme_name = settings_dict["defaults"]["game_theme"]
    if "farkle_" in theme_name:
        theme_name = theme_name.replace("farkle_", "")
    sg.theme(f'farkle_{theme_name}')

    players.player_1.skin = settings.player1_col
    players.player_2.skin = settings.player2_col
    settings_dict["user_set"] = {}

    to_json.output_to_file(settings_dict, "settings")

    # Need to reset the speed. I'm doing it in a bad way, tricky to get it right for both viewing/editing and actual roll speed. Should redo it.
    settings.player_roll_speed = settings.player_roll_speed / 1000
    settings.computer_roll_speed = settings.computer_roll_speed / 1000
    remove_player_colour_gifs()


class playerInst:

    def __init__(self, player_name, skin = None):

        self.name = player_name
        self.turn_score = 0
        self.turn_record = {}
        self.roll_count = 0
        self.skin = skin
        self.turn_count = 0
        self.game_score = 0
        self.wins = 0
        self.losses = 0
        self.held_dice = None
        self.roll_speed = 0.2

        self.playstyle = None

    def __repr__(self):
        return f"<player: {self.name} // held_score: {self.held_dice} // turn_score: {self.turn_score}>"

class playerClass:

    def __init__(self):
        self.is_singleplayer = True
        self.default_playstyle = "harpoon"

        self.players:set = set()
        self.player_1:playerInst = None
        self.player_2:playerInst = None
        self.current:playerInst = None
        self.opponent:playerInst = None
        self.autoplay = False
        self.playstyles:list = ["standard", "harpoon"]

        self.total_games:int = int()
        self.total_turns:int = int()
        self.tally:dict[int, str] = {}

    def scoreline(self):
        return f"Current player: {self.current.name}\nScores: {self.player_1.name}: {self.player_1.game_score} / {self.player_2.name}: {self.player_2.game_score}"


    def __repr__(self):
        return f"Players: {self.players} Current player: {self.current.name}"

def update_roll_speeds():

    print(f"updating_roll_speeds\nplayer 1 start: {players.player_1.roll_speed} // {players.player_2.roll_speed}")
    print(f"Existing roll speed: player_roll_speed: {settings.player_roll_speed} // players.player_1.roll_speed: {players.player_1.roll_speed}")
    players.player_1.roll_speed = settings().player_roll_speed
    if players.is_singleplayer:
        players.player_2.roll_speed = settings().computer_roll_speed
    else:
        players.player_2.roll_speed = settings().player_roll_speed
    print(f"updating_roll_speeds\nplayer 1 start: {players.player_1.roll_speed} // {players.player_2.roll_speed}")

def init_classes(player1 = "player_1", player2 = "player_2", player1_col = "red", player2_col = "blue"):

    if players.players:
        players.players = set()

    if players.is_singleplayer:
        player2 = players.default_playstyle

    player_1 = playerInst(player1, skin=player1_col)

    players.players.add(player_1)
    players.player_1 = player_1
    players.current = player_1

    player_2 = playerInst(player2, skin=player2_col)
    players.players.add(player_2)
    players.player_2 = player_2
    players.opponent = player_2

    if players.is_singleplayer:
        players.autoplay = player_2
        player_2.playstyle = players.default_playstyle
        player_2.name = player_2.playstyle + "Bot"

    update_roll_speeds()

    return dict({"player_1": player_1, "player_2": player_2})

def apply_playstyle(player:playerInst, turn_score, available_dice:set[die]):

    think_aloud = True

    playstyle_rules = {

        "harpoon": {
            "take_risk": {
                f"I'm over {points_to_win/2} points behind": (players.opponent.game_score - (points_to_win/2)) > player.game_score,
                "My opponent too close to winning": players.opponent.game_score > 3200,
                "I don't have enough score from this roll": player.turn_score + turn_score < (points_to_win/8)
            },
            "requirements": {
                "in_dice": [1, 5],
                "all_dice_used": True
                }
        }
    }
    use_dice = set()
    if player.playstyle and player.playstyle in playstyle_rules:
        for risk_reason in playstyle_rules[player.playstyle]["take_risk"]:
            if not playstyle_rules[player.playstyle]["take_risk"][risk_reason]:
                continue
            for item in playstyle_rules[player.playstyle]["requirements"]:
                if use_dice:
                    break
                if item == "in_dice":
                    if 1 in playstyle_rules[player.playstyle]["requirements"][item]:
                        onedice = list(i for i in available_dice if i.value == 1)
                        if onedice:
                            use_dice.add(onedice[0])
                            turn_score = 100
                        elif 5 in playstyle_rules[player.playstyle]["requirements"][item]:
                                onedice = list(i for i in available_dice if i.value == 5)
                                if onedice:
                                    use_dice.add(onedice[0])
                                    turn_score = 50

    if use_dice:
        if think_aloud and len(available_dice) > 3:
            sleep(.02)
        return turn_score, use_dice

    return turn_score, None

def get_score(player:playerInst=None, autoplay_dice=None, get_score=True, test_only=False, end_turn=False): # if print_result, send roll to json
    """returns held_score (int) and used_dice (set)"""
    if autoplay_dice:
        dice_selection = set(autoplay_dice)
    else:
        dice_selection = set(i for i in dice.dice if i.held and not i.used)

    if not dice_selection:
        return 0, set(), None
    print_output=None
    matches = {}
    held_score = 0
    vals = set(i.value for i in dice_selection)

    score_dict = {i:None for i in dice_selection}

    used_dice = set()
    if len(vals) == 6:
        used_dice = dice_selection
        score_dict = {i:"full house" for i in dice_selection}
        matches["full house"] = ({1: {1: 1500}}) # I know this isn't what a full house is, but i'm using it like this anyway. It's not used within the game so the term is arbitrary.
        held_score += 1500

    elif len(vals) == 5:
        matched = set(i for i in (1, 2, 3, 4, 5) if i in vals)
        if not matched or not len(matched) == 5:
            matched = list(i for i in (2, 3, 4, 5, 6) if i in vals)
        if matched and len(matched) == 5:
            for item in matched:
                if item not in score_dict.values():
                    for i in dice_selection:
                        if i.value == item:
                            score_dict[i] = item
                            used_dice.add(i)
                            break
            held_score += 750
            matches["small straight"] = ({"small_straight": {1: 750}})

    for item in vals:
        count = sum(1 for die in dice_selection if die.value == item and die not in used_dice)
        if count >= 3:
            multimatch = set(die for die in dice_selection if die.value == item and die not in used_dice)
            for i, die in enumerate(multimatch):
                if item == 1:
                    used_dice.add(die) # allows 5 1's exclusively
                    match_count = i
                else:
                    if i < 4:
                        match_count = i
                        used_dice.add(die) # to only add up to 4 of a multi selection, only 3 and 4 of a kind  works.
                        if count == 3:
                            multiplier = 1
                        else:
                            multiplier = 2
            if item != 1:
                held_score += item * (100 * multiplier)
                matches["three (or four) of a kind"] = ({item: {count: item * (100 * multiplier)}})
            else:
                #print(f"Match count: {match_count}")
                held_score += 1000 * (match_count-1)
                matches["three (or four) of a kind"] = ({item: {count: int(1000 * (match_count-1))}})

    remaining_dice_selection = set(i for i in dice_selection if i not in used_dice)
    if remaining_dice_selection:
        #pos.print_error(f"Remaining dice: {remaining_dice_selection}", 2)
        vals = set(i.value for i in remaining_dice_selection)
        for item in vals:
            count = sum(1 for die in remaining_dice_selection if die.value == item and die not in used_dice and not die.used)
            if count:
                if item == 1:
                    #pos.print_error(f"item == 1", 1)
                    used_dice.update(set(i for i in remaining_dice_selection if i.value == item and i not in used_dice and not i.used))
                    #matches["single ones"] = ({item: {count: int(100 * count)}})
                    held_score += 100 * count
                    matches["single ones"] = ({item: {count: int(100 * count)}})
                elif item == 5:
                    #pos.print_error(f"item == 5", 2)
                    used_dice.update(set(i for i in remaining_dice_selection if i.value == item and i not in used_dice and not i.used))
                    #matches["single fives"] = ({item: {count: int(50 * count)}})
                    held_score += 50 * count
                    matches["single fives"] = ({item: {count: int(50 * count)}})

    if players.is_singleplayer and player.playstyle and (used_dice and len(used_dice) != len(dice_selection)): # only for NPC
        held_score, updated_dice = apply_playstyle(player, held_score, dice_selection)
        if updated_dice:
            used_dice = updated_dice

    if not end_turn and not test_only:
        to_json.collect_turndata(matches=matches, dice_rolled=dice_selection, roll_score=held_score)

    if not matches and not test_only:
        player.turn_score = 0

    if get_score:
        player.turn_score += held_score

    if end_turn and not test_only:
        to_json.collect_turndata(matches=matches, dice_rolled=dice_selection, roll_score=held_score, turn_end=end_turn)
    return held_score, used_dice, print_output

def clear_held_and_used_dice(reset_val=True):

    for d in dice.dice:
        if reset_val:
            d.value = 9
        d.used = False
        d.held = False
        d.held_previously = False

def update_tally():

    players.tally[players.total_turns] = (players.current.name, players.current.game_score)


def held_die_now_used_die(die_inst:die):
    die_inst.used = True
    die_inst.held = False

def mark_used(in_loop):
    for die in in_loop:
        held_die_now_used_die(die_inst=die)

    in_loop.clear()

def take_roll(player:playerInst):

    player.game_score += player.turn_score
    if settings.export_to_file:
        to_json.collect_turndata(turn_end=True)


rules = "\nA `straight` (`1, 2, 3, 4, 5, 6`) is 1500 points\nA `small straight` (either `1, 2, 3, 4, 5` or `2, 3, 4, 5, 6`) is 750 points\n" \
"Three-of-a-kind is `number x 100` (eg `3, 3, 3` is 300 points.)\nFour of a kind is `2x (number x 100)` (eg `3, 3, 3, 3` is 600 points)\n\n" \
"1's and 5's are special: All other numbers are only valuable as part of one of the combinations above, and cannot be chosen alone.\n" \
"But -- a `1` on its own is worth 100 points, and a `5` on its own is worth 50 points. \n\n" \
"* 1's are extra special: instead of 'number x 100', they are 'number x 1000' ie, `1, 1, 1, 1` is 2000 points.\n\n" \
"You must select at least one die each roll. If there is no valid die to select, you will bust, ending your turn and losing your points from that turn.\n" \
"After selecting one or more die, you can choose to keep the points from those dice, or reroll the dice left over to try to get more points.\n\n" \
"If you use all of your dice in one turn, you can reroll everything and keep the existing score - as long as you don't bust!\n\n\n" \
f"First player to {points_to_win} points wins! And whoever lost goes first next round.\n"

#### GUI ####

#https://github.com/PySimpleGUI/PySimpleGUI/issues/4909 <- change button bg col and button mouseover col.


def collapse(layout, key, visible=False):
    return sg.pin(sg.Column(layout, key=key, visible=visible, element_justification="center", vertical_alignment="center", expand_y=True))

def add_dots(dot_size=std_dot_size):
    dot_colour = theme_data.theme_dict[sg.theme()]["dot_colour"]
    dot_instance = sg.Text('•', font=(f"courier {dot_size} bold"), text_color=dot_colour, auto_size_text=True, pad=0, justification="centre")
    return dot_instance

def make_vert_dots(size1=std_dot_size, size2=std_dot_size, size3=std_dot_size):
    return [[add_dots(size1)], [add_dots(size2)], [add_dots(size3)]]

def make_horz_dots(size1=std_dot_size, size2=std_dot_size, size3=std_dot_size):
    return [[add_dots(size1), add_dots(size2), add_dots(size3)]]


def make_window() -> tuple[str['exit'], None] | tuple[None, str['use_settings']]:

    def run_gif_anim(gif_filepath, die_key):

        image = Image.open(gif_filepath)
        frames = image.n_frames
        accumImage = sg.tk.PhotoImage(file=gif_filepath, format=f'gif -index 0')
        data = [accumImage]
        for i in range(0, frames):
            deltaImage = sg.tk.PhotoImage(file=gif_filepath, format=f'gif -index {i}')
            accumImage.tk.call(accumImage, 'copy', deltaImage)
            data.append(accumImage.copy())
            window[die_key].update(data=accumImage)
            #print(f"players.current.roll_speed: {players.current.roll_speed}")
            sleep(players.current.roll_speed)
            window.refresh()

    def play_farkle_intro():

        if dice.showing_farkle:
            print("Already showing farkle.")
            return

        print("Showing farkle animation")
        for char in ("f", "a", "r", "k", "l", "e"):
            gif_file = gif_data.farkle_bust_gifs[char]
            run_gif_anim(gif_file, farkle_to_no[char])

    def roll_animated_die(die_inst=None, farkle=False, bust=False, used=False, farkle_from_bust=False, farkle_from_current=False, from_held=False, from_used=False, force_rolls=None):

        import os
        if farkle:
            print("Rolling farkle")
            play_farkle_intro()
            return

        make_other = []
        target_dir = f"{os.getcwd()}\\dice_graphics\\random_rolls\\"
        target_file = target_dir + "temp.gif"

        if isinstance(die_inst, str):
            die_inst = dice.get_die_inst(die_inst)

        from make_dice_images import make_combination_image, transition_to_from, button_held, button_used

        if die_inst.held:
                other_colour = button_held
        elif die_inst.used:
            other_colour = button_used
        else:
            other_colour = players.current.skin

        if farkle_from_bust or farkle_from_current:
            if farkle_from_bust:
                char = bust_text[f"die_{die_inst.place_no}"]
            else:
                char = str(die_inst.value)

            make_other.append(str(char))
            f_char = str(no_to_farkle[f"die_{die_inst.place_no}"])
            make_other.append(f_char)
            make_other = "".join(make_other)
            anim_frames = transition_to_from([], outgoing_char=str(char), outgoing_colour=other_colour, incoming_char=f_char, incoming_colour=other_colour, start_roll=False, blank_before_incoming=False,
                        end_roll=False, output_name = "temp", start_from_blank=False, end_with_blank=False, subfolder="random_rolls\\", continue_with_list=True) # runn twice to have it repeat the farkle roll
            transition_to_from(anim_frames, outgoing_char=f_char, outgoing_colour=other_colour, incoming_char=f_char, incoming_colour=other_colour, start_roll=False, blank_before_incoming=False,
                        end_roll=False, output_name = "temp", start_from_blank=False, end_with_blank=False, continue_with_list=False, subfolder="random_rolls\\")
            dice.showing_farkle=True

        elif bust:
            bust_char = bust_text[f"die_{die_inst.place_no}"]
            make_other.append(str(die_inst.value))
            make_other.append(bust_char)
            make_other = "".join(make_other)

            make_combination_image(make_other=make_other, make_other_colour = other_colour, other_subfolder="random_rolls\\", end_blank=False)

        elif used or from_held or from_used:

            make_other.append(str(die_inst.value))
            make_other.append(str(die_inst.value))
            make_other = "".join(make_other)
            if from_held:
                #print(f"FROM HELD: {from_held} // {die_inst}")
                transition_to_from([], outgoing_char=str(die_inst.value), outgoing_colour=button_held, incoming_char=str(die_inst.value), incoming_colour=players.current.skin, start_roll=False, blank_before_incoming=False,
                        end_roll=False, output_name = "temp", start_from_blank=False, end_with_blank=False, continue_with_list=False, subfolder="random_rolls\\")
                die_inst.held=False
            elif from_used:
                transition_to_from([], outgoing_char=str(die_inst.value), outgoing_colour=button_used, incoming_char=str(die_inst.value), incoming_colour=players.current.skin, start_roll=False, blank_before_incoming=False,
                        end_roll=False, output_name = "temp", start_from_blank=False, end_with_blank=False, continue_with_list=False, subfolder="random_rolls\\")
                die_inst.used = False
            else:
                transition_to_from([], outgoing_char=str(die_inst.value), outgoing_colour=button_held, incoming_char=str(die_inst.value), incoming_colour=button_used, start_roll=False, blank_before_incoming=False,
                        end_roll=False, output_name = "temp", start_from_blank=False, end_with_blank=False, continue_with_list=False, subfolder="random_rolls\\")

        else:
            ### If die is used or held, make the first roll from-state, then continue on. Total number of rolls == same either way so the timings work.
            random_selection = random.choices(range(1,7), k=3)
            make_other = list(str(i) for i in random_selection)

            original_val = str(die_inst.value)
            if original_val == "9":
                make_other.insert(0, str(no_to_farkle[f"die_{die_inst.place_no}"]))
            else:
                make_other.insert(0, str(die_inst.value))

            if force_rolls:
                die_inst.value = force_rolls
                make_other.append(str(die_inst.value))
            else:
                die_inst.value = int(make_other[-1])

            make_other = "".join(make_other)

            if die_inst.held or die_inst.used:
                anim_frames = transition_to_from([], outgoing_char=make_other[0], outgoing_colour=other_colour, incoming_char=make_other[1], incoming_colour=players.current.skin, start_roll=False, blank_before_incoming=False,
                            end_roll=False, output_name = "temp", start_from_blank=False, end_with_blank=False, subfolder="random_rolls\\", continue_with_list=True)
                make_combination_image(make_farkle = False, make_bust=False, make_other=make_other[1:], make_other_colour = players.current.skin, other_subfolder="random_rolls\\", end_blank=False, anim_frames=anim_frames)
            else:
                make_combination_image(make_farkle = False, make_bust=False, make_other=make_other, make_other_colour = players.current.skin, other_subfolder="random_rolls\\", end_blank=False)
            dice.showing_farkle=False

        if make_other:

            run_gif_anim(target_file, f"die_{die_inst.place_no}")

    def hold_dice(die_inst):

        dice.hold(die_inst)
        if die_inst.held:
            window[f"die_{die_inst.place_no}"].update(filename=gif_data.held_still[str(die_inst.value)])
        else:
            window[f"die_{die_inst.place_no}"].update(filename=gif_data.player_1_stills[str(die_inst.value)] if players.player_1 == players.current else gif_data.player_2_stills[str(die_inst.value)])


    def roll_dice(used_dice=None, reroll_all=False, prereroll=False) -> None:

        print_points_line(string_print="Rolling...")

        force_rolls = False

        if prereroll:
            for die_inst in dice.dice:
                if die_inst.used or die_inst.held:
                    if die_inst.held:
                        print(f"Die is held: {die_inst}")
                        roll_animated_die(die_inst, from_held=True)
                        die_inst.held = False
                    else:
                        print(f"Die is held: {die_inst}")
                        roll_animated_die(die_inst, from_used=True)
                        die_inst.used = False
                die_inst.held_previously = False
            dice.showing_farkle=False

        for die_inst in dice.dice:
            if die_inst.used and not reroll_all:
                continue
            if used_dice and die_inst in used_dice and not reroll_all:
                continue
            else:
                if force_rolls:
                    roll_animated_die(die_inst, force_rolls=die_inst.place_no)
                else:
                    roll_animated_die(die_inst)

            if reroll_all:
                die_inst.used = False
        """ Want to get roll data directly from here, I think."""
        players.current.roll_count += 1
        to_json.format_dicerolls()

        #print("\nend of roll_dice\n")

    def make_button(width:float=std_btn, height:float=std_btn, key_str:str="Pause", tooltip_str = '', key=None):
        if not key:
            key_upper = key_str.upper()
            key_formatting = str("-" + key_upper + '-')
        else:
            key_formatting = key
        #sg.Button("Hello", , use_ttk_buttons=True)
        return sg.Button(key_str, key=key_formatting, mouseover_colors=settings.t.theme_dict[sg.theme()]["button_mouseover"], use_ttk_buttons=True, size=(width,height), font=(f"courier {std_dot_size} bold"), tooltip=tooltip_str if tooltip_str else None)

    def make_die(key_str:str="1"):

        key_str = key_str
        button = sg.Image(filename=gif_data.farkle_stills[no_to_farkle[key_str]], size=(100,100), enable_events=True, key=key_str)
        #CHANGEME: Set this to the blank farkle colour image, then roll into the character gif.

        return button

    def mid_gap():
        return [[sg.Canvas(size=(12,14))]]


    def round_over(winner:playerInst):
        winner.wins += 1
        clear_held_and_used_dice()
        window["print_player_stats"].update(players.scoreline())#f"Current player: {players.current.name}\nScores: {players.player_1.name}: {players.player_1.game_score} / {players.player_2.name}: {players.player_2.game_score}")

        print("Sending to collect_turndata in round_over")
        to_json.collect_turndata(game_end=True)

        def new_game_window():
            new_game_layout = [
                [sg.Stretch(), sg.Text(f"{winner.name} wins this round with", font=(f"courier {std_dot_size + 2} bold")), sg.Stretch()],
                [sg.Stretch(), sg.Text(f"{winner.game_score} points!", font=(f"courier {std_dot_size + 2} bold")), sg.Stretch()],
                [sg.VStretch()],
                [sg.Text("New Game?", font=(f"courier {std_dot_size+2} bold"))],
                [sg.Button("Yes", key="-NEW_GAME_YES-", use_ttk_buttons=True, size=(8,1), font=(f"courier {std_dot_size +2} bold")), sg.Button("No", key="-NEW_GAME_NO-", use_ttk_buttons=True, size=(8,1), font=(f"courier {std_dot_size +2} bold"))],
                [sg.Text('', font=(f"courier {std_dot_size} bold"), key="newgame_print")],
                [sg.VStretch()],
            ]

            new_game_window = sg.Window("New Game?", new_game_layout, element_justification="center", finalize=True, modal=True, keep_on_top=True)
            event, values = new_game_window.read()

            while True:
                if event == "-NEW_GAME_YES-":
                    dice.showing_farkle=False
                    new_game_window.close()
                    return True

                elif event == "-NEW_GAME_NO-":
                    new_game_window.close()
                    return False

        if new_game_window():

            for p in players.players:
                p.game_score = 0
                p.turn_count = 0
            players.total_turns = 0
            players.tally = {}
            window["print_player_stats"].update(players.scoreline())#f"Current player: {players.current.name}, scores: {players.player_1.name}: {players.player_1.game_score} / {players.player_2.name}: {players.player_2.game_score}")

            window["output_line"].update("Starting a new game!")
            window.refresh()

        else:
            window["output_line"].update(f"Thanks for playing! Final scores: {players.player_1.name}: {players.player_1.game_score} points, {players.player_1.wins} games won // {players.player_2.name}: {players.player_2.game_score} points, {players.player_2.wins} games won")
            return "game_over"


    def reset_for_new_turn(bust=False):
        """Returns "end_game" if not starting a new game, "new_game" if starting a new game."""
        update_tally()
        for d in dice.dice:
            d.held_previously = False
        tally_entries, tally_entries_second = update_tally_entries()
        window["tally_table_P1"].update(tally_entries)
        if tally_entries_second:
            window["tally_table_P2"].update(tally_entries_second, visible=True)

        to_json.collect_turndata(dice_rolled=dice.dice, bust=bust, turn_end=True) # only initial if first roll
        print_points_line('')
        print_output_text(f"{players.current.name} ends their turn with {players.current.turn_score} points, for a total score of {players.current.game_score} points.")
        #print_output_text(f"{print_colour.playernm(players.current, "output")} ends their turn with a score of [[{players.current.game_score}]].")

        if not dice.showing_farkle:
            for die_inst in dice.dice:
                roll_animated_die(die_inst, farkle_from_current=True)

        players.current.turn_score = 0

        players.current.roll_count = 0
        players.opponent.roll_count = 0

        if players.current.game_score >= points_to_win:
            if round_over(winner=players.current):
                return "end_game"

        players.total_turns += 1
        players.current, players.opponent = players.opponent, players.current

        clear_held_and_used_dice()

        # CHANGEME: needs to roll from current value to farkle image.
        window["print_player_stats"].update(players.scoreline())#f"Current player: {players.current.name}\nScores: {players.player_1.name}: {players.player_1.game_score} / {players.player_2.name}: {players.player_2.game_score}")


    def print_points_line(score='', bust=False, string_print='', print_banked = False):

        if string_print:
            point_value = string_print
        elif not bust:
            if score:
                point_value = f"Points from this roll: {score} / Banked score: {players.current.turn_score}"
            else:
                if print_banked:
                    point_value = f"Banked score: {players.current.turn_score}"
                else:
                    point_value = ''
        else:
            point_value = f"{players.current.name} busts!! They lose their banked score and end their turn."
        window["point_output"].update(point_value)
        return

    def print_output_text(text=''):
        #output_line_str, key="output_line"
        output_line_str = text
        window["output_line"].update(output_line_str)

    def clear_prints(print_banked = True):

        print_points_line(print_banked=print_banked)
        print_output_text()


    def take_score_and_end_turn(get_turnscore = True):
        clear_prints()
        if get_turnscore:
            _, _, _ = get_score(players.current, set(i for i in dice.dice if i.held), get_score=True, end_turn=True)
        take_roll(players.current)
        outcome = reset_for_new_turn() # in take_score_and_end_turn
        return outcome


    def gui_autoplay(player:playerInst, used_dice):
        """for player_2 to be PC controlled."""

        if not used_dice:
            print_points_line(string_print=f"{players.current.name} is starting their turn.")

        def start_turn() -> None | str['bust']:
            print_output_text(text='')
            sleep(.2)
            used_dice_count = sum(1 for d in dice.dice if d.used)
            if used_dice_count == 6:
                print_output_text(f"{players.current.name} used all their dice; rerolling all.")
                roll_dice(reroll_all=True)
                clear_held_and_used_dice(reset_val=False)
                #roll_animated_die(die_inst, from_used=True)
            else:
                roll_dice()
            _, used_dice, _ = get_score(players.current, set(i for i in dice.dice if not i.used), get_score=False)
            sleep(.3)
            if not used_dice:
                return "bust"
            print_points_line(string_print="Selecting dice to hold...")

        clear_held_and_used_dice()

        while True:

            if start_turn():
                return "bust", None

            unused_dice = set(i for i in dice.dice if not i.used)

            has_potential, used_dice, output_text = get_score(player, unused_dice, get_score=False)

            if not has_potential: # should not get here, as it should get caught by start_turn
                return "bust", None

            for die_inst in dice.dice:
                if die_inst in used_dice:
                    die_inst.held = True
                    print_output_text(text=output_text)
                    if die_inst.held and not die_inst.held_previously:
                        window[f"die_{die_inst.place_no}"].update(filename=gif_data.held_still[str(die_inst.value)])
                        window.refresh()
                    sleep(.3)
                print_points_line(has_potential)
                window.refresh()


            score, used_dice, output_text = get_score(player, used_dice)
            for die_inst in dice.dice:
                if die_inst in used_dice:
                    print_output_text(text=output_text)
                    held_die_now_used_die(die_inst=die_inst)
                    window[f"die_{die_inst.place_no}"].update(filename=gif_data.used_still[str(die_inst.value)])
                    die_inst.used_previously=False
                    window.refresh()
                    sleep(.15)

            print_points_line(score)
            window.refresh()

            used_dice_count = sum(1 for d in dice.dice if d.used)

            if used_dice_count > 3:
                unused = set(i for i in dice.dice if not i.used)
                if unused:
                    for i in unused:
                        if i.value == 5:
                            player.turn_score += 50
                            i.used = True
                            used_dice.add(i)
                        elif i.value == 1:
                            player.turn_score += 100
                            i.used = True
                            used_dice.add(i)

            mark_used(used_dice)
            for die_inst in dice.dice:
                if die_inst in used_dice:
                    print_output_text(text=output_text)
                    window[f"die_{die_inst.place_no}"].update(filename=gif_data.used_still[str(die_inst.value)])
                    die_inst.held_previously=False
                    window.refresh()
                    sleep(.15)

            used_dice_count = sum(1 for d in dice.dice if d.used)

            if (used_dice_count) == 6:
                if player.game_score + player.turn_score >= points_to_win:
                    print_output_text(f"{players.current.name} used all their dice and is taking the current score.")
                    window.refresh()
                    return "end_turn", None

                #roll_dice(reroll_all=True)
                #print_output_text(f"{players.current.name} used all their dice; rerolling all.")
                #for die_inst in dice.dice:
                    #roll_animated_die(die_inst, from_used=True)
                #clear_held_and_used_dice()
            else:
                if (used_dice_count < 4 and (player.game_score + player.turn_score < points_to_win)) or player.turn_score < points_to_win/8:
                    window["output_line"].update("Rolling again.")
                else:
                    window["output_line"].update(f"{player} ends their turn with {player.turn_score} points.")
                    sleep(.5)
                    return "end_turn", None

    def update_tally_entries():

        tally_entries = []
        tally_entries_second = []

        if players.tally:
            for turncount in players.tally:
                (playername, score) = players.tally[turncount]

                tally_entries.append([f"[Turn {turncount+1}]  {playername} has {score} points"])

        if len(tally_entries) > 20:
            tally_entries_second = tally_entries[int(len(tally_entries)/2):]
            tally_entries = tally_entries[:(len(tally_entries) - len(tally_entries_second))]

        elif len(tally_entries) > 10:
            tally_entries_second = tally_entries[10:]
            tally_entries = tally_entries[:10]

        return tally_entries, tally_entries_second

    def get_tally():
        tally_entries, tally_entries_second = update_tally_entries()
        col_width = (len(players.player_1.name) if players.player_1.name and len(players.player_1.name) > len(players.player_2.name) else len(players.player_2.name)) + len("Turn x:   = xxxx points")

        tally_alt:str = theme_data().theme_dict[sg.theme()]["alt_tally_bg"]
        tally_bg:str = theme_data().theme_dict[sg.theme()]["BACKGROUND"]

        return [sg.Stretch(), sg.Table(values = [tally_entries], key="tally_table_P1", display_row_numbers=False, headings=[''], expand_y=True, hide_vertical_scroll=True, def_col_width = col_width, auto_size_columns=False, justification="left", background_color=tally_bg, alternating_row_color=tally_alt, text_color=tally_text_col, row_height=22), sg.Table(values = [tally_entries_second], key="tally_table_P2", display_row_numbers=False, headings=[''], expand_y=True, hide_vertical_scroll=True, def_col_width = col_width, auto_size_columns=False, visible=tally_alt if tally_entries_second else False, justification="left", background_color=tally_bg, alternating_row_color=tally_alt, text_color=tally_text_col), sg.Stretch()]


    def rules_window(): #separate window so it can be left open during play if desired
        #rules_panel = [[sg.Canvas(size=(widest_measure,2), pad=2)],
        #            [sg.Text(text=rules, expand_x=True, expand_y=True, text_color=theme_data().theme_dict[sg.theme()]["gold_text"], justification="center")],
        #            [sg.Stretch(), sg.Text(text="[ Note: You can keep the rules open while you play if you like. ]", justification="right")]
        #            ]

        def make_rules_panel():
            """ right_click_menu=["Open text as plain text file", "Close"] """
            rules_image = f'{os.getcwd()}\\rules_{settings.game_theme.replace("farkle_", "")}.png'
            with Image.open(rules_image) as im:
                size = im.size
                height = im.height
                width = im.width
            graph = sg.Graph(canvas_size=size, graph_top_right=(width, 0), graph_bottom_left=(0, height), background_color=settings.t.theme_dict[sg.theme()]['BACKGROUND'], right_click_menu=[["menu"], ["Open text as plain text file", "Close"]], key="rules_graph", metadata={"image_filepath": rules_image, "height": im.height, "width": im.width})
            return [graph]

        rules_main = [[sg.Column([make_rules_panel()])]]

        rules_layout = [[sg.Frame(title="", key="rules_window", layout=rules_main, font=("courier", std_dot_size, "bold"), relief="groove", pad=(5), border_width=5)]]

        rules_window = sg.Window(' rules ••', rules_layout, keep_on_top=True, finalize=True, margins=(10,10), grab_anywhere=True, no_titlebar=False, use_custom_titlebar=True,
                                 titlebar_background_color=theme_data().theme_dict[sg.theme()]["title_bg"], titlebar_text_color=theme_data().theme_dict[sg.theme()]["gold_text"], titlebar_font="courier 10 bold", titlebar_icon=png_icon,
                                 right_click_menu_background_color=theme_data().theme_dict[sg.theme()]["title_bg"], right_click_menu_selected_colors=settings.t.theme_dict[sg.theme()]["button_mouseover"], right_click_menu_text_color=theme_data().theme_dict[sg.theme()]["gold_text"])

        not_drawn = True
        timeout_rate = 50
        while True:
            event, _ = rules_window.read(timeout=timeout_rate)
            if not_drawn:
                graph = rules_window["rules_graph"] # type: sg.Graph
                graph.draw_image(filename=graph.metadata["image_filepath"], location=(0,0))
                not_drawn = False
                timeout_rate = 1000
            if event == "Open text as plain text file":
                import subprocess
                osCommandString = "notepad.exe RULES.txt"
                subprocess.Popen(osCommandString)
            if event == "Close":
                rules_window.close()
                break
            if rules_window.is_closed():
                break

    def clear_print_lines_before_close():
        sleep(.8)
        window["print_player_stats"].update("")
        print_points_line()
        window.refresh()
        sleep(.3)
        print_output_text()
        sleep(2)
        window.refresh()
        sleep(.5)

    def check_for_close_event(event):
        if event == sg.WIN_CLOSED or event == '-EXIT-' or event == "__TITLEBAR CLOSE__":
            return "exit"

    def roll_to_bust():

        print_points_line(bust=True)
        for d in dice.dice:
            roll_animated_die(d, bust=True)
        sleep(.2)
        for d in dice.dice:
            roll_animated_die(d, farkle_from_bust=True)

    def roll_to_used():
        for d in dice.dice:
            if d.used and not d.held_previously:
                roll_animated_die(d, used=True)
                d.held_previously = True


    dice_display = [[make_die("die_1"),
                    sg.Column(layout=mid_gap()),
                    make_die("die_2"),
                    sg.Column(layout=mid_gap()),
                    make_die("die_3"),
                    sg.Column(layout=mid_gap()),
                    make_die("die_4"),
                    sg.Column(layout=mid_gap()),
                    make_die("die_5"),
                    sg.Column(layout=mid_gap()),
                    make_die("die_6"),
                    ]]

    tally_board = [get_tally()]

    settings_rules_and_exit = [[make_button(width=std_btn, height=1, key_str="Settings", tooltip_str = "Settings:\n  * change single/two player\n  * set computer player mode\n  * change player names + colours  \n  * change colour theme."), add_dots(), make_button(width=std_btn, height=1, key_str="Rules"), add_dots(), sg.HSeparator(color=gold), add_dots(), make_button(width=std_btn, height=1, key_str="Exit")],
                    [sg.Stretch(), sg.Text(text=players.scoreline(), key="print_player_stats", font=(f"courier {int(std_dot_size) + 2} bold"), text_color=theme_data().theme_dict[sg.theme()]["gold_text"], pad=0, justification="center", size=(60,2)), sg.Stretch()],
                    [sg.Canvas(size=(widest_measure,2))],
                    [sg.HSeparator(color=gold)],
                    [sg.Canvas(size=(widest_measure,2))],
                    [sg.Column(layout=make_vert_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), vertical_alignment="center"),
                     sg.Column(key="dice_layout", layout=dice_display, justification="c", vertical_alignment="center"),
                     sg.Column(layout=make_vert_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), vertical_alignment="center")]]

    point_output = [
                    [sg.Stretch(), sg.HSeparator(color=gold), sg.Stretch()],
                    [sg.Canvas(size=(widest_measure,2), pad=2)],
                    [sg.Stretch(), sg.Text(point_value, key="point_output", font=(f"courier {int(std_dot_size) + 4} bold"), pad=0, justification="center"), sg.Stretch()],
                    [sg.Canvas(size=(widest_measure,2), pad=2)],
                    [sg.Stretch(), sg.HSeparator(color=gold), sg.Stretch()]
                    ]

    roll_take_and_output_print =      [
                     [
                     sg.Stretch(), sg.Column(layout=make_horz_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), pad=0),
                     # changed 'take' to 'end turn' for clarity.
                     make_button(width=std_btn, height=1, key_str="Roll", tooltip_str=" Bank the score from the selected dice, and roll the remaining dice again - try not to bust! \n\n If you bust, the banked score will not be added to your game score and your turn will end. "), make_button(width=std_btn, height=1, key="-TAKE-", key_str="End Turn", tooltip_str="Add the banked score from this round (if any) and the score from the selected dice to your final score, and end your turn."),
                     sg.Column(layout=make_horz_dots(size1=int(std_dot_size)+4, size2=int(std_dot_size)+2, size3=std_dot_size)),
                     sg.Stretch()],

                     [sg.Canvas(size=(widest_measure,2), pad=2)],
                     [sg.HSeparator(color=gold)],
                     [sg.Canvas(size=(widest_measure,2), pad=2)],
                    [sg.Stretch(), sg.Text(output_line_str, key="output_line", font=(f"courier {int(std_dot_size) + 2} bold"), pad=0, justification="center"), sg.Stretch()],
                    [sg.Canvas(size=(200,1)), add_dots(), sg.HSeparator(color=gold), add_dots(), sg.Canvas(size=(200,1))],
                    [sg.Stretch(), sg.Text(text="A game by HarpoonLobotomy, 2026.", font="courier 10 bold", text_color=theme_data().theme_dict[sg.theme()]["gold_text"]), sg.Stretch()],
                       [sg.Canvas(size=(widest_measure,2))],
                    [sg.VStretch()]
                    ]

    tally = [
            [sg.Stretch(), sg.T(SYMBOL_UP, enable_events=True, k='-OPEN SEC1-', font = "courier 12 bold"), sg.T('Tally Board', enable_events=True, k='-OPEN SEC1-TEXT', font = "courier 12 bold"), sg.Stretch()],
            [collapse(tally_board, '-SEC1-')]
            ]

    farkle_main_screen = [
            [sg.Column(layout=settings_rules_and_exit, justification="center")], [sg.Column(layout=point_output, justification="center")], [sg.Column(layout=roll_take_and_output_print, justification="center", expand_x=True)], [sg.Column(layout=tally, justification="center")]
        ]

    layout = [[sg.Frame(title="", layout=farkle_main_screen, font=("courier", std_dot_size, "bold"), relief="groove", pad=(5), border_width=5)]]

    window = sg.Window(' farkle ••', layout, keep_on_top=True, finalize=True, alpha_channel=1.0, disable_close=True, grab_anywhere=False, no_titlebar=False, use_custom_titlebar=True, titlebar_background_color=theme_data().theme_dict[sg.theme()]["title_bg"], titlebar_text_color=theme_data().theme_dict[sg.theme()]["gold_text"], titlebar_font="courier 10 bold", titlebar_icon=png_icon)
    window['-TAKE-'].bind("<Return>", "_Enter")

    round_started = False
    dice.showing_farkle=False
    opened1 = False
    window['-SEC1-'].update(visible=False)
    to_json.start_game()

    """
    All print lines (in order of appearance):

        window["print_player_stats"].update(f"Current player: {players.current.name}, scores: {players.player_1.name}: {players.player_1.game_score} / {players.player_2.name}: {players.player_2.game_score}")
        print_points_line(string_print='200 points from this roll')
        print_output_text(text=f"{players.current.name} is starting their turn.")

    """

    while True:

        event, values = window.read(timeout=500)

        if check_for_close_event(event):

            if not window.is_closed():
                clear_prints()

            return "exit", None

        if not round_started and not dice.showing_farkle:
            print("not round started and not dice.showing_farkle")
            roll_animated_die(farkle=True)
            dice.showing_farkle=True
            print("Ended roll_animated from not round_started and not dice.showing_farkle")

        used_dice = None
        if players.is_singleplayer and players.current == players.player_2:
            round_started = True
            autoplay_loop_event, values = window.read(timeout=100) # exists so it checks immediately after the autoplay fn runs instead of having to wait for it to do the scoring etc first. Not perfect but improved.
            outcome, used_dice = gui_autoplay(players.current, used_dice) # game_won end_turn bust
            if check_for_close_event(autoplay_loop_event):
                return "exit", None
            if outcome:
                #print(f"OUTCOME of turn {players.total_turns}: {outcome}")
                if outcome == "end_turn":
                    round_started = take_score_and_end_turn(get_turnscore=False)
                    if check_for_close_event(autoplay_loop_event):
                        return "exit", None
                    if round_started and round_started == "end_game":
                        #clear_print_lines_before_close()
                        window.close()
                        return "exit", None
                        #break

                elif outcome == "bust":
                    roll_to_bust()

                    if check_for_close_event(autoplay_loop_event):
                        return "exit", None
                    window.refresh()
                    sleep(.5)
                    players.current.turn_score = 0
                    if check_for_close_event(autoplay_loop_event): # added a number of these so it has different opportunities to notice and exit to limit the user wait after clicking close.
                        return "exit", None
                    reset_for_new_turn(bust=True) # ln 1664 if player2 busts
                    round_started = False
                elif outcome == "game_won":
                    round_over(players.current)

        if not round_started and (event == "-ROLL-" or settings.roll_on_start):
            autoplay_loop_event, values = window.read(timeout=100)

            roll_animated_die(farkle=True)
            clear_held_and_used_dice()
            print_output_text(text=f"{players.current.name} is starting their turn.")
            sleep(.2)
            if check_for_close_event(autoplay_loop_event):
                return "exit", None
            print_points_line(string_print='', print_banked=False)
            roll_dice()
            to_json.collect_turndata(dice_rolled=dice.dice) # only initial if first roll
            score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice), get_score=False)
            round_started = True
            print_output_text(text=output_str)
            if not used_dice:
                print_points_line(bust=True)
                roll_to_bust()
                if check_for_close_event(autoplay_loop_event):
                    return "exit", None
                sleep(.8)
                reset_for_new_turn(bust=True) #line 1692 if bust out the gate
                round_started = False
            print_points_line(string_print="Select dice to hold...")

        if event and event.startswith('-OPEN SEC1-'):
            opened1 = not opened1
            window['-OPEN SEC1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_UP)
            window['-SEC1-'].update(visible=opened1)

        if "die_" in event and round_started:
            print(f"DIE IN EVENT: {event}")
            clear_prints(print_banked=True)
            die_inst = dice.get_die_inst(event)
            if die_inst.used:
                continue
            hold_dice(die_inst)
            score, _, output_str = get_score(players.current, set(i for i in dice.dice if i.held), get_score=False, test_only=True)
            print_output_text(text=output_str)
            print_points_line(score, print_banked=True)

        if event == "-ROLL-" and round_started:
            held_dice = set(i for i in dice.dice if i.held)
            if not held_dice:
                print_output_text("You must hold at least one die before rolling.")
            else:
                preroll_score, new_used_dice, _ = get_score(players.current, held_dice, get_score=False)
                if preroll_score == 0:
                    print_output_text("You must hold at least one die viable before rolling.")
                    continue

                mark_used(new_used_dice)
                for i in dice.dice:
                    if i.held:
                        i.held=False
                roll_to_used()
                if check_for_close_event(event):
                    return "exit", None
                used_dice = set(i for i in dice.dice if i.used)
                if used_dice and len(used_dice) == 6:
                    print_output_text(f"{players.current.name} used all their dice; rerolling all.")
                    roll_dice(reroll_all=True)
                    clear_held_and_used_dice(reset_val=False)
                else:
                    roll_dice(used_dice)

                score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice if not i.used), get_score=False)
                print_output_text(text=output_str)
                if check_for_close_event(event):
                    return "exit", None
                if not used_dice:
                    roll_to_bust()
                    print_points_line(bust=True)
                    sleep(.8)
                    reset_for_new_turn(bust=True) # line 1746 if player busts
                    round_started = False
                else:
                    players.current.turn_score += preroll_score
                clear_prints(print_banked=True)

        if event == "-TAKE-":
            print("Pressed 'take'")
            if not players.current.turn_score and not (dice.dice and any(i.held for i in dice.dice)): # ""any(i.held for i in dice.dice)"" oh so that's a use for any. Good.
                print_output_text("You can't take nothing if there are valid scoring dice.")
                continue
            round_started = take_score_and_end_turn()
            if round_started and round_started == "end_game":
                #clear_print_lines_before_close()
                return "exit", None

        if event == "-SETTINGS-":
            clear_prints()
            window.close()
            return None, "use_settings"

        if event == "-RULES-":
            rules_window()


def settings_window():

    def make_settings_button(width:float=std_btn, height:float=std_btn, key:str="", key_str:str="Pause", tooltip_str='', metadata=None):
        if key:
            key_formatting = key
        else:
            key_upper = key_str.upper()
            key_formatting = str("-" + key_upper + '-')
        return sg.Button(auto_size_button=True, button_text = key_str, key=key_formatting, mouseover_colors=settings.t.theme_dict[sg.theme()]["button_mouseover"], use_ttk_buttons=True, size=(width,height), font=(f"courier {std_dot_size} bold"), disabled_button_color = "#756C5F", tooltip=tooltip_str if tooltip_str else None, metadata=metadata)

    def make_playstyle_buttons():
        playstyle_buttons = []
        for style in players.playstyles:
            playstyle_buttons.append(sg.Canvas(size=(10,2), pad=2, background_color=canvas_col))
            playstyle_buttons.append(make_settings_button(width=std_btn, height=1, key=style, key_str=f"[{style}]"))
        playstyle_buttons.append(sg.Canvas(size=(10,2), pad=2, background_color=canvas_col))
        return playstyle_buttons

    def settings_collapse(layout, key, visible=False):
        """
        Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
        :param layout: The layout for the section
        :param key: Key used to make this seciton visible / invisible
        :return: A pinned column that can be placed directly into your layout
        :rtype: sg.pin
        """
        if visible:
            collapsable = [
            [sg.Column(layout, key=key + "_inner", element_justification="center", background_color=region_3_col, pad=0)],
            ]
        else:
            collapsable =[
                [sg.Column(layout, key=key + "_inner", element_justification="center", background_color=region_3_col, pad=0)]]
        return sg.pin(sg.Column(layout=collapsable, key=key, visible=visible, justification="center", background_color=region_2_col, pad=0))


    test_die_path = f"{os.getcwd()}\\dice_graphics\\farkle_in_one_testing_quicker.gif"
    def test_die(pc_or_comp):
        return [sg.Image(filename = test_die_path, key = f"test_die_anim_{pc_or_comp}", enable_events=True)]

    def set_speed(pc_or_comp):

        return [
        [sg.Text(text=f"The current speed is `{getattr(settings, pc_or_comp)*100:.1f}`.\nClick the die to have it animate at this speed.", key=f"speed_text_{pc_or_comp}")],
        [sg.Stretch()],
        test_die(pc_or_comp),
        [sg.Stretch()],
        [sg.Input(default_text=f'{getattr(settings, pc_or_comp)*100:.1f}', key=f"speed_input_{pc_or_comp}")],
        [sg.Ok(key=f"set_input_{pc_or_comp}", bind_return_key=False), sg.Cancel(key=f"cancel_input_{pc_or_comp}")]
        ]


    change_speed_buttons = [[sg.VStretch()],
        [sg.VStretch()],
        [make_settings_button(width = std_btn*3, height = 1, key_str = f"Change player roll speed ({(settings.player_roll_speed*100):.1f})", key="change_play_roll"),
        make_settings_button(width = std_btn*3+3, height = 1, key_str = f"Change computer roll speed ({(settings.computer_roll_speed*100):.1f})", key="change_comp_roll")],
        ]

    advanced = [
        [settings_collapse(layout=change_speed_buttons, key="speed_buttons", visible=True)],
        [settings_collapse(layout = set_speed("player_roll_speed"), key="player_roll_spd"), settings_collapse(layout = set_speed("computer_roll_speed"), key="comp_roll_spd")],
        [sg.VStretch()],
        [sg.HSeparator(color=gold)],
        [sg.VStretch()],
        [make_settings_button(width=std_btn*5, height=1, metadata = settings.roll_on_start,
            key_str="Automatically start the first roll" if settings.roll_on_start else "Not starting rolling immediately", key="start_roll_immediately",
                tooltip_str="If turned off, the game won't start until the player clicks 'Roll'.")],
        [sg.VStretch()],
        [sg.HSeparator(color=gold)],
        [sg.VStretch()],
        [make_settings_button(width=std_btn*5, height=1, metadata = settings.export_to_file,
            key_str="Not exporting play data to file" if not settings.export_to_file else "Exporting play data to file", key="export_to_file",
                tooltip_str="Export the data from your games to a .json file.")],
        [sg.VStretch()]
    ]

    singleplayer = [
                     [sg.Canvas(size=(widest_measure,22), pad=2, background_color=canvas_col)],
                    [sg.VStretch()],
                     [sg.HSeparator(color=gold)],
                     [sg.Text("Currently, the game is single player. What do you want it to be?" if players.is_singleplayer else "Currently, the game is two-player. What do you want it to be?", text_color=theme_data().theme_dict[sg.theme()]["gold_text"])],
                     [sg.Canvas(size=(widest_measure,2), pad=2)],
                     [make_settings_button(width=std_btn, height=1, key="choose_single", key_str="Single player"), sg.Canvas(size=(10,2), pad=2, background_color=canvas_col), make_settings_button(width=std_btn, height=1, key="choose_two", key_str="Two human players")],
                     [sg.Canvas(size=(widest_measure,2), pad=2)],
                     [sg.Text("Note: Changing to/from single player mode will reset the game.", text_color=theme_data().theme_dict[sg.theme()]["gold_text"])],
                     [sg.HSeparator(color=gold)],
                     [sg.VStretch()],
                     [sg.Canvas(size=(widest_measure,10), pad=2, background_color=canvas_col)]
                    ]

    mode = [
                    [sg.VStretch()],
                     [sg.HSeparator(color=gold)],
                     [sg.Canvas(size=(widest_measure-30,10), pad=0, background_color=canvas_col)],
                     [sg.Text(f"Currently, the computer is using the playstyle `{players.default_playstyle}`.\nWhat do you want it to be?", justification="center", text_color=theme_data().theme_dict[sg.theme()]["gold_text"])],
                     [sg.Canvas(size=(widest_measure-30,6), pad=0, background_color=canvas_col)],
                     make_playstyle_buttons(),
                     [sg.Canvas(size=(widest_measure-30,6), pad=0, background_color=canvas_col)],
                     [sg.HSeparator(color=gold)],
                     [sg.Canvas(size=(widest_measure-30,6), pad=0, background_color=canvas_col)],
                     [sg.Text(text="'Standard' is the basic game mode:\n  the computer will simply take the best dice it sees each roll.\n\n'Harpoon' is an emulation of the author, which uses strategy across multiple rolls each turn.", justification="center", text_color=theme_data().theme_dict[sg.theme()]["gold_text"])],
                     [sg.VStretch()]
                    ]

    names = [
                    [sg.VStretch()],
                     [sg.Canvas(size=(widest_measure,6), pad=2, background_color=canvas_col)],
                     [sg.HSeparator(color=gold)],
                     [sg.Text(f"Player 1 is currently named `{players.player_1.name}`.\nPlayer 2 is currently named `{players.player_2.name}`", justification="center", text_color=theme_data().theme_dict[sg.theme()]["gold_text"])],
                     [sg.Text(f"Enter new names below to change them, or set a new colour for that player.", justification="center", text_color=theme_data().theme_dict[sg.theme()]["gold_text"])],
                     [sg.Canvas(size=(widest_measure,2), pad=2, background_color=canvas_col)],
                     [sg.Input(default_text=players.player_1.name, key="player_1_name", focus=True, enable_events=True), sg.Input(players.player_1.skin, key="player_1_col_text", enable_events=True, visible=False), sg.ColorChooserButton(f"{players.player_1.skin}", target="player_1_col_text", key="player_1_colour", button_color=players.player_1.skin, border_width=1, size=(8,1), font=(f"courier {std_dot_size} bold"), tooltip="Choose a colour for Player 1.\n(Colour will update after saving settings.)")],
                     [sg.Canvas(size=(widest_measure,2), pad=2, background_color=canvas_col)],
                     [sg.Input(default_text=players.player_2.name, key="player_2_name", enable_events=True), sg.Input(players.player_2.skin, key="player_2_col_text", enable_events=True, visible=False), sg.ColorChooserButton(f"{players.player_2.skin}", target="player_2_col_text", key="player_2_colour", button_color=players.player_2.skin, border_width=1, size=(8,1), font=(f"courier {std_dot_size} bold"), tooltip="Choose a colour for Player 2.\n(Colour will update after saving settings.)")],
                     [sg.Canvas(size=(widest_measure,2), pad=2, background_color=canvas_col)],
                     [sg.HSeparator(color=gold)],
                     [sg.VStretch()]
                    ]

    themes = [
                    [sg.VStretch()],
                    [sg.Canvas(size=(widest_measure,25), pad=2, background_color=canvas_col)],
                     [sg.HSeparator(color=gold)],
                     [sg.Stretch(), sg.Text(f"Currently, the theme is `{sg.theme().replace("farkle_", "")}`", justification="center", text_color=theme_data().theme_dict[sg.theme()]["gold_text"]), sg.Stretch()],
                     [sg.Canvas(size=(widest_measure,2), pad=2, background_color=canvas_col)],
                     [sg.Stretch(), make_settings_button(width=std_btn, height=1, key="choose_tan", key_str="TAN"), sg.Stretch(), make_settings_button(width=std_btn, height=1, key="choose_navy", key_str="NAVY"), sg.Stretch(), make_settings_button(width=std_btn, height=1, key="choose_arcade", key_str="ARCADE"), sg.Stretch()],
                     [sg.Canvas(size=(widest_measure,2), pad=2, background_color=canvas_col)],
                     [sg.Stretch(), sg.Text("[Click 'Save changes' to apply a new theme.]", text_color=theme_data().theme_dict[sg.theme()]["gold_text"]), sg.Stretch()],
                     [sg.Canvas(size=(widest_measure,2), pad=2, background_color=canvas_col)],
                     [sg.HSeparator(color=gold)],
                     [sg.VStretch()]
                    ]

    blank_settings = [
                    [sg.Canvas(size=(20, 50), background_color=canvas_col)],
                    [sg.Text(text="[ Change settings in the sections above, and click 'Save changes' to save and update. ]\n[ Click 'Return without saving' to keep existing settings. ]\n[ Click 'restore settings' to return to the original default settings in all categories. ]\n\n(All three buttons below will return you to the game.)", justification="center", text_color=theme_data().theme_dict[sg.theme()]["gold_text"])]
    ]
    theme_sections = [
                    [sg.Canvas(size=(554, 0), background_color=canvas_col)],
                    [settings_collapse(blank_settings, "blank"), settings_collapse(singleplayer, '-SEC1-'), settings_collapse(mode, '-MODE-'), settings_collapse(names, '-NAMES-'), settings_collapse(themes, '-THEMES-'), settings_collapse(advanced, '-ADVANCED-')],
                    [sg.Canvas(size=(554, 1), background_color=canvas_col, pad=0)]
    ]

    settings_options = [
                    [sg.HSeparator(color=gold)],
                    [
                        make_settings_button(width=std_btn, height=1, key="panel_single_player", key_str="Single player"), add_dots(), sg.HSeparator(color=gold), add_dots(),
                        make_settings_button(width=std_btn, height=1, key="panel_mode", key_str="Computer mode"), add_dots(), sg.HSeparator(color=gold), add_dots(),
                        make_settings_button(width=std_btn, height=1, key="panel_names", key_str="Player names"), add_dots(), sg.HSeparator(color=gold), add_dots(),
                        make_settings_button(width=std_btn, height=1, key="panel_themes", key_str="Colour themes")
                        ],
                    [sg.Stretch()],
                    [make_settings_button(width=std_btn*2, height=1, key="panel_advanced", key_str="Advanced settings")],
                    [sg.HSeparator(color=gold)],
                    [sg.Column(layout = theme_sections, size=(570, 245), justification="center", element_justification="center", background_color=region_1_col, pad=((4,2),(2,2)))],
                    [sg.HSeparator(color=gold)],

                    [sg.Stretch(), add_dots(), make_settings_button(width=std_btn, height=1, key="leave", key_str="Save changes", tooltip_str="Return to game with the new settings."), add_dots(), make_settings_button(width=std_btn, height=1, key="leave_no_save", key_str="Return without saving", tooltip_str="Closing the settings window without applying changes."), add_dots(), make_settings_button(width=std_btn, height=1, key="restore", key_str="[Restore defaults]", tooltip_str="Restore settings to defaults. Will restart the game."), add_dots(), sg.Stretch()]
                    ]

    settings_main = [
                     [sg.Column(settings_options, justification="center", element_justification="center", pad=5, background_color=region_3_col)]
                    ]

    settings_layout = [[sg.Frame(title=" farkle settings •• ", key="settings_window", layout=settings_main, font=("courier", std_dot_size, "bold"), relief="groove", pad=(5), border_width=5, expand_x=True, element_justification="center")]]

    settings_window = sg.Window(' settings ••', settings_layout, keep_on_top=True, finalize=True, alpha_channel=1.0, disable_close=False, grab_anywhere=True, no_titlebar=True, use_custom_titlebar=True, titlebar_background_color=theme_data().theme_dict[sg.theme()]["title_bg"], titlebar_text_color=theme_data().theme_dict[sg.theme()]["gold_text"], titlebar_font="courier 10 bold", titlebar_icon=png_icon)
    settings_dict = {}

    settings_window["blank"].update(visible=True)

    def swap_panels(list_to_close, panel_to_open="ADVANCED"):
        for panel in list_to_close:
            if settings_window[panel].visible:
                settings_window[panel].update(visible=False)

        if settings_window[panel_to_open].visible:
            settings_window[panel_to_open].update(visible=False)
            settings_window['blank'].update(visible=True)
        else:
            settings_window['blank'].update(visible=False)
            settings_window[panel_to_open].update(visible=True)


    while True:
        event, values = settings_window.read(timeout=1000)

        if values and values.get("player_1_name"):
            settings_dict["change_names"] = values

        if event:
            if event == "restore":
                settings_dict["restore_defaults"] = True
                settings_window.close()
                return settings_dict

            if event in players.playstyles:
                settings_dict["set_playstyle"] = event
                for style in players.playstyles:
                    settings_window[style].update(disabled=True if event == style else False)

            if event.startswith("panel_"):
                if event == "panel_advanced":
                    settings_window["start_roll_immediately"].update(button_color=settings_window["start_roll_immediately"].DisabledButtonColor if not settings_window["start_roll_immediately"].metadata else settings.t.theme_dict[sg.theme()]["BUTTON"])
                    settings_window["export_to_file"].update(button_color=settings_window["export_to_file"].DisabledButtonColor if not settings_window["export_to_file"].metadata else settings.t.theme_dict[sg.theme()]["BUTTON"])
                    swap_panels(list_to_close = ['-MODE-', '-NAMES-', '-THEMES-', '-SEC1-'], panel_to_open="-ADVANCED-")

                if event == "panel_single_player":

                    swap_panels(list_to_close = ['-MODE-', '-NAMES-', '-THEMES-', "-ADVANCED-"], panel_to_open="-SEC1-")

                    if settings_window['-SEC1-'].visible:
                        settings_window["choose_single"].update(disabled=True if players.is_singleplayer else False)
                        settings_window["choose_two"].update(disabled=False if players.is_singleplayer else True)

                if event == "panel_mode":
                    swap_panels(list_to_close = ['-SEC1-', '-NAMES-', '-THEMES-', "-ADVANCED-"], panel_to_open='-MODE-')

                    if settings_window["-MODE-"].visible:
                        for style in players.playstyles:
                            settings_window[style].update(disabled=True if players.default_playstyle == style else False)

                if event == "panel_names":
                    swap_panels(list_to_close = ['-SEC1-', '-MODE-', '-THEMES-', "-ADVANCED-"], panel_to_open='-NAMES-')

                if event == "panel_themes":
                    swap_panels(list_to_close = ['-SEC1-', '-MODE-', '-NAMES-', "-ADVANCED-"], panel_to_open='-THEMES-')

                    if settings_window["-THEMES-"].visible:
                        settings_window["choose_tan"].update(disabled=True if "tan" in sg.theme() else False)
                        settings_window["choose_navy"].update(disabled=True if "navy" in sg.theme() else False)
                        settings_window["choose_arcade"].update(disabled=True if "arcade" in sg.theme() else False)

            pc_or_comp = "player_roll_speed", "computer_roll_speed"

            if "player_roll_speed" in event or "computer_roll_speed" in event:
                if "player_roll_speed" in event:
                    pc_or_comp = "player_roll_speed"
                else:
                    pc_or_comp = "computer_roll_speed"
                #print(f"EVENT FROM THIS: {event} // values: {values}")
                if event == f"cancel_input_{pc_or_comp}":
                    settings_window["comp_roll_spd"].update(visible = False)
                    settings_window["player_roll_spd"].update(visible = False)
                    if "player" in event:
                        settings_window["change_play_roll"].update(f"Change player roll speed ({settings.player_roll_speed*100})")
                    else:
                        settings_window["change_comp_roll"].update(f"Change computer roll speed ({settings.computer_roll_speed*100})")

                    settings_window["speed_buttons"].update(visible = True)
                if event == f"set_input_{pc_or_comp}":
                    settings_dict[f"set_input_{pc_or_comp}"] = values[f"speed_input_{pc_or_comp}"]
                    settings_window[f"speed_text_{pc_or_comp}"].update(f"The current speed is `{values[f'speed_input_{pc_or_comp}']}`.\nClick the die to have it animate at this speed.")
                    if "player" in event:
                        settings_window["change_play_roll"].update(f"Change player roll speed ({values[f'speed_input_{pc_or_comp}']})")
                    else:
                        settings_window["change_comp_roll"].update(f"Change computer roll speed ({values[f'speed_input_{pc_or_comp}']})")

                    settings_window["player_roll_spd"].update(visible = False)
                    settings_window["comp_roll_spd"].update(visible = False)
                    settings_window["speed_buttons"].update(visible = True)

                if event == f"test_die_anim_{pc_or_comp}":
                    settings_dict[f"set_input_{pc_or_comp}"] = values[f"speed_input_{pc_or_comp}"]
                    settings_window[f"speed_text_{pc_or_comp}"].update(f"The current speed is `{values[f'speed_input_{pc_or_comp}']}`.\nClick the die to have it animate at this speed.")
                    #print("Animating gif")
                    image = Image.open(test_die_path)
                    frames = image.n_frames
                    accumImage = sg.tk.PhotoImage(file=test_die_path, format=f'gif -index 0')
                    data = [accumImage]
                    for i in range(0, frames):
                        deltaImage = sg.tk.PhotoImage(file=test_die_path, format=f'gif -index {i}')
                        accumImage.tk.call(accumImage, 'copy', deltaImage)
                        data.append(accumImage.copy())
                        settings_window[f"test_die_anim_{pc_or_comp}"].update(data=accumImage)
                        sleep(float(values[f"speed_input_{pc_or_comp}"])/100)
                        settings_window.refresh()

            if event == "change_play_roll" or event == "player_roll_spd":
                if settings_window["player_roll_spd"].visible:
                    settings_window["player_roll_spd"].update(visible = False)
                    settings_window["speed_buttons"].update(visible = True)
                else:
                    settings_window["comp_roll_spd"].update(visible = False)
                    settings_window["speed_buttons"].update(visible = False)
                    settings_window["player_roll_spd"].update(visible = True)

            if event == "change_comp_roll":
                if settings_window["comp_roll_spd"].visible:
                    settings_window["comp_roll_spd"].update(visible = False)
                    settings_window["speed_buttons"].update(visible = True)
                else:
                    settings_window["speed_buttons"].update(visible = False)
                    settings_window["player_roll_spd"].update(visible = False)
                    settings_window["comp_roll_spd"].update(visible = True)

                settings_dict["player_roll_spd"] = values
                """Pop open a window to enter a new value. Perhaps with a die gif to test with as you change it."""

                settings_dict["comp_roll_spd"] = values
                """Pop open a window to enter a new value. Perhaps with a die gif to test with as you change it."""

            if event == "start_roll_immediately":
                print(f"event: {event} // value; {values}")
                state = not settings_window["start_roll_immediately"].metadata
                settings_window["start_roll_immediately"].metadata = state
                print(f'settings_window["start_roll_immediately"].metadata: {settings_window["start_roll_immediately"].metadata}')
                settings_dict["start_roll_immediately"] = state
                settings_window["start_roll_immediately"].update("Not starting rolling immediately" if not state else "Automatically start the first roll", button_color=settings_window["start_roll_immediately"].DisabledButtonColor if not state else settings.t.theme_dict[sg.theme()]["BUTTON"])

            if event == "export_to_file":
                print(f"event: {event} // value; {values}")
                state = not settings_window["export_to_file"].metadata
                settings_window["export_to_file"].metadata = state
                print(f'settings_window["export_to_file"].metadata: {settings_window["export_to_file"].metadata}')
                settings_dict["export_to_file"] = state
                settings_window["export_to_file"].update("Not exporting play data to file" if not state else "Exporting play data to file", button_color=settings_window["export_to_file"].DisabledButtonColor if not state else settings.t.theme_dict[sg.theme()]["BUTTON"])

            if event == "choose_single":
                settings_dict["set_singleplayer"] = True
                settings_window["choose_single"].update(disabled=True)
                settings_window["choose_two"].update(disabled=False)

            if event == "choose_two":
                settings_dict["set_singleplayer"] = False
                settings_window["choose_single"].update(disabled=False)
                settings_window["choose_two"].update(disabled=True)

            if event == "choose_tan":
                settings_dict["set_theme"] = "farkle_tan"
                settings_window["choose_tan"].update(disabled=True)
                settings_window["choose_navy"].update(disabled=False)
                settings_window["choose_arcade"].update(disabled=False)

            if event == "choose_navy":
                settings_dict["set_theme"] = "farkle_navy"
                settings_window["choose_tan"].update(disabled=False)
                settings_window["choose_navy"].update(disabled=True)
                settings_window["choose_arcade"].update(disabled=False)

            if event == "choose_arcade":
                settings_dict["set_theme"] = "farkle_arcade"
                settings_window["choose_tan"].update(disabled=False)
                settings_window["choose_navy"].update(disabled=False)
                settings_window["choose_arcade"].update(disabled=True)

            if event == "leave":
                settings_window.close()
                return settings_dict

            if event == "leave_no_save":
                settings_window.close()
                return "no_save"


def update_settings_json(update_data:dict):

    """updates JSON with provided dict. Only the keys provided will be updated, and only if the value is different to the current value."""
    json_data = to_json.load_json("settings")
    print(f"JSON DATA: {json_data}")
    for key, value in update_data.items():
        json_data["user_set"][key] = value

    to_json.output_to_file(json_data, "settings")


def apply_settings(settings_dict):
    """applies settings to relevant game vars/classes, and updates JSON if enabled and necessary."""
    update_json_dict = {}

    print(f"SETTINGS DICT:\n\n{settings_dict}\n\n")

    for action, data in settings_dict.items():

        if "roll_speed" in action:
            print(f"Roll speed given: {data}")
            print(f"Existing roll speed: player_roll_speed: {settings.player_roll_speed} // players.player_1.roll_speed: {players.player_1.roll_speed}")
            if action == "set_input_computer_roll_speed":
                settings.computer_roll_speed = float(data)/100
                update_json_dict["computer_roll_speed"] = int(float(data)*10)
            if action == "set_input_player_roll_speed":
                settings.player_roll_speed = float(data)/100
                update_json_dict["player_roll_speed"] = int(float(data)*10)
            print(f"New roll speed: player_roll_speed: {settings.player_roll_speed} // players.player_1.roll_speed: {players.player_1.roll_speed}")
            update_roll_speeds()

        if action == 'export_to_file':
            print(f"action == export to file, data: {data}")
            update_json_dict["export_to_file"] = data

        if action == "restore_defaults":
            print("Restoring settings to defaults.")
            restore_defaults()
            init_classes(player1 = settings.player1_name, player2 = settings.player2_name, player1_col = settings.player1_col, player2_col = settings.player2_col)
            dice.init_dice()

        if action == "set_singleplayer":
            print(f"action is set_singleplayer: true/false: `{data}`")
            if players.is_singleplayer != data:
                update_json_dict["is_singleplayer"] = data
                players.is_singleplayer = data
                init_classes(players.player_1.name, '', player1_col = "blue", player2_col = "red")

        if action == "change_names":
            for name in data:
                if data[name]:
                    if "_name" in name:
                        if name == "player_1_name":
                            if data[name] != players.player_1.name:
                                update_json_dict["player1_name"] = data[name]
                                players.player_1.name = data[name]

                        elif name == "player_2_name":
                            if data[name] != players.player_2.name:
                                update_json_dict["player2_name"] = data[name]
                                players.player_2.name = data[name]

                    if "col_text" in name:
                        player_num = name.split("_")[1]
                        colour = data[name]
                        colour_changed = False
                        if "colour: " in colour:
                            colour = colour.split("colour: ")[1]
                        if player_num == "1":
                            if players.player_1.skin != colour:
                                players.player_1.skin = colour
                                update_json_dict["player1_col"] = colour
                                gif_data.player_1_path = f"{os.getcwd()}\\dice_graphics\\num_by_colour\\{players.player_1.skin}\\"
                                colour_changed = True
                        elif player_num == "2":
                            if players.player_2.skin != colour:
                                players.player_2.skin = colour
                                update_json_dict["player2_col"] = colour
                                gif_data.player_2_path = f"{os.getcwd()}\\dice_graphics\\num_by_colour\\{players.player_2.skin}\\"
                                colour_changed = True
                        if colour_changed:
                            colour_dice_sets()

        if action == "set_theme":
            if data != sg.theme():
                update_json_dict["game_theme"] = data
                sg.theme(new_theme=data)

        if action == "set_playstyle":
            if players.default_playstyle != data:
                update_json_dict["playstyle"] = data
                players.default_playstyle = data
                if players.is_singleplayer:
                    players.player_2.playstyle = data
                    players.player_2.name = f"{data}Bot"

    if update_json_dict:
        update_settings_json(update_json_dict)
    init_settings()

def remove_random_rolls_on_close():

    random_rolls = f"{os.getcwd()}\\dice_graphics\\random_rolls\\"
    filecount = len(os.listdir(random_rolls))
    print(f"Removing random roll gifs from `{random_rolls}`")
    for file in os.listdir(random_rolls):
        if not ".gif" in file:
            continue
        filepath = random_rolls + file
        os.remove(filepath)
    print(f"Removed {filecount} random roll gifs. Closing.")

def main_gui():

    # Add a waiting window here #
    init_settings()

    global players
    players = playerClass()

    init_classes(player1 = settings.player1_name, player2 = settings.player2_name, player1_col = settings.player1_col, player2_col = settings.player2_col)

    colour_dice_sets()

    force_settings = False

    while True:

        if force_settings:
            settings_dict = settings_window()
            if settings_dict and settings_dict == "no_save":
                break

        else:
            close_window, use_settings = make_window()
            if close_window:
                break
            elif use_settings:
                settings_dict = settings_window()
                if settings_dict and not isinstance(settings_dict, str):
                    apply_settings(settings_dict)

    remove_random_rolls_on_close()
    from make_dice_images import o
    o.save_data()

main_gui()
