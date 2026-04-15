"""simple text-based farkle game
started April 2026 //  [gui version] v 1.1 // harpoonlobotomy"""

# Command to build a .exe file:
#   [cd to py file dir first] pyinstaller --onefile --noupx --icon farkle_gui.ico farkle_gui.pyw

# have commented out to_json throughout, add it back later.
from time import sleep
import random
import FreeSimpleGUI as sg

die_refresh_val = 0.135
points_to_win = 4000

canvas_col = None#"white"
region_1_col = None#"red"
region_2_col = None#"magenta"
region_3_col = None#"blue"
v_stretch_col = None#"green"
h_stretch_col = None#"yellow"


window_is_closed = False

class settings:

    player1_name:str = None
    player1_col:str = None
    player2_name:str = None
    player2_col:str = None
    playstyle:str = None
    is_singleplayer:bool = None
    computer_think_aloud:bool = None
    output_file:str = None
    game_theme:str = None

    def init(self, settings_dict):

        for item in settings.__annotations__: # counted here as long as the type is given, apparently. Can't be the best way to do this but seems to be working so will go with it.
            setattr(settings, item, settings_dict["user_set"][item] if settings_dict["user_set"].get(item) else settings_dict["defaults"][item])
        #print(f"SETTINGS VARS: {vars(settings)}")
        """self.player1_name = settings_dict["user_set"]["player1_name"] if settings_dict["user_set"].get("player1_name") else settings_dict["defaults"]["player1_name"]
        self.player2_name = settings_dict["user_set"]["player2_name"] if settings_dict["user_set"].get("player2_name") else settings_dict["defaults"]["player2_name"]
        self.playstyle = settings_dict["user_set"]["playstyle"] if settings_dict["user_set"].get("playstyle") else settings_dict["defaults"]["playstyle"]
        self.is_singleplayer = settings_dict["user_set"]["is_singleplayer"] if settings_dict["user_set"].get("is_singleplayer") else settings_dict["defaults"]["is_singleplayer"]
        self.computer_think_aloud = settings_dict["user_set"]["computer_think_aloud"] if settings_dict["user_set"].get("computer_think_aloud") else settings_dict["defaults"]["computer_think_aloud"]
        self.output_file = settings_dict["user_set"]["output_file"] if settings_dict["user_set"].get("output_file") else settings_dict["defaults"]["output_file"]
"""

class theme_data():

    def __init__(self):
        pass

    eggplant = "#3E2857",
    navy = "#284157"
    ivory = "#E0DAC5"
    theme_dict:dict = {
        "farkle_navy": {'BACKGROUND': navy,
                    'TEXT': "#B08F23",#"#25775f",
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
                    "gold_text": "#ffd768"},

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
                    "gold_text": "#442D15"
                    },

        "farkle_arcade": {'BACKGROUND': "#38354a",#31374e",
                    'TEXT': "#de4507",
                    'INPUT': "#45523F",
                    'TEXT_INPUT': "#f5db74",
                    'SCROLL': "#003e9b",
                    'BUTTON': ('black', "#ffda57"),##ffd657"),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 3,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0,
                    'dot_colour': "#d35700",
                    'font': "courier 14 bold",
                    "alt_tally_bg": "#433e5e",
                    "title_bg": "#382b43",#362b43",
                    #"title_bg": "#31374e",
                    "gold_text": "#f0c762",# "#ffd365",
                    'ACCENT1': '#FF0266','ACCENT2': '#FF5C93','ACCENT3': '#C5003C',
                    }}

    def init_themes(self):


        sg.theme_add_new('farkle_tan', self.theme_dict["farkle_tan"])
        sg.theme_add_new('farkle_navy', self.theme_dict["farkle_navy"])
        sg.theme_add_new('farkle_arcade', self.theme_dict["farkle_arcade"])
        #sg.theme('farkle_tan')


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
    theme_data()
    theme_data.init_themes(theme_data)
    sg.theme(f'farkle_{theme_name}')


#sg.theme('farkle_tan')
#sg.theme('farkle_arcade')

gold = "#ffff7f" # "gold"
std_dot_size=10
widest_measure = 340#560#340
half_measure = (widest_measure/2)-5
std_btn = 10
num_pad_w = 20
num_pad_h = 8
numbers_size = 40
border_lg = 6
size_text="small"
small_hide=False
tooltip_str="Press to change to small version"
restart_str="[Restart]"
pause_str="[Paused]"

bg_brown="#332b26"
bg_blue = "#36554E"#"darkblue"
numbers_colour="yellow"
button_mouseover="#105C26"
button_held = "#F8DC5E"
button_used = "#666354"
#player_1_die = settings.player1_col#"#5AC280"
#player_2_die = settings.player2_col#"#5A90C2"

die_bust_col = ('white', "#330303")

dice_dict = {}

die_1 = 1
die_2 = 2
die_3 = 3
die_4 = 4
die_5 = 5
die_6 = 6

point_value = ''
output_line_str = ''

SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'

bust_text = {
    "die_1": "-",
    "die_2": "B",
    "die_3": "U",
    "die_4": "S",
    "die_5": "T",
    "die_6": "-",
}

preroll_text = {
    "die_1": "F",
    "die_2": "A",
    "die_3": "R",
    "die_4": "K",
    "die_5": "L",
    "die_6": "E",
}

tally_text_col = None#"#653635"

png_icon = "farkle_icon_48.png"
#png_icon = "farkle_gui.ico"


def make_play_area():

    #print("\033[s", end='')
    #print("\033[6n", end='') # reports current cursor position

    error_line = "0"
    error = f"\033[{int(error_line)};1f"
    start_line = "6" # before this is space for errors

    points = f"\033[{int(start_line)-1};1f\033[2;32m"
    dice_str = f"\033[{int(start_line) + 3};7f"
    prompt = f"\033[{int(start_line) + 6};1f"
    inputstr = f"\033[{int(start_line) + 8};1f"
    output = f"\033[{int(start_line) + 10};1f"

    global pos
    pos = pos_data(error, points, dice_str, prompt, inputstr, output)

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

class die:
    def __init__(self, place_number = 1, skin=None):
        self.value = 1
        self.place_no = place_number
        self.held = False
        self.used = False
        self.skin = skin

    def __repr__(self):
        return f"<place_no: {self.place_no} / value: {self.value} / used: {self.used} / held: {self.held}>"

class dice_data:

    def __init__(self):

        self.skin = None
        self.dice:set[die] = set()
        self.by_no:dict[int, die] = {}

        self.force_dicerolls = False

    def init_dice(self):

        for i in range(1, 7):
            die_inst = die(place_number=i, skin=self.skin)
            self.dice.add(die_inst)
            self.by_no[i] = die_inst

        #self.by_no = {die.place_no: die for die in self.dice}

    def print_updated(self, die = None, skin = None):

        def print_die(die, skin):
            if isinstance(die, int):
                die = self.by_no[die]
            if isinstance(die, str):
                die = self.by_no[int(die)]

            if skin:
                die_skin = colours[skin] if colours.get(skin) else skin
            else:
                die_skin = die.skin if die.skin else colours.get("red") # should allow for per-die skin, as well as default skin (which can be set by dice set on init or by player)
                if die.held:
                    die_skin = colours.get(print_colour.held_dice) # green for held dice
                    if "[1m" in die_skin:
                        die_skin = die_skin.replace("[1m", "[")
                    #die_skin = "\033[2m" + die_skin # dim the held dice a bit to make them more visually distinct from unheld dice
                elif die.used:
                    die_skin = colours.get(print_colour.used_dice)
                    if "[1m" in die_skin:
                        die_skin = die_skin.replace("[1m", "[")
                    #die_skin = "\033[2m" + die_skin # dim the held dice a bit to make them more visually distinct from unheld dice

            pos.print_dice(text = f"[  {die.value}  ]", die=die, skin=die_skin)
            sleep(.01)

        if not die:
            for i in range(1, 7):
                print_die(i, skin)

        else:
            print_die(die, skin)


    def set_default_val(self):

        for die in dice.dice:
            if dice.skin and (not die.skin or die.skin == "default" or die.skin != dice.skin):
                die.skin = dice.skin

            #die.place_no = int(str(val)) ## Why was I ever resetting the /place_no/???
            die.value = die.place_no # place 1-6 in that order
            dice.print_updated(die, skin=print_colour.pre_diceroll)
            sleep(.08)
            print()

    def hold(self, die_inst): # selecting by place_no; if there was a graphic, they would scatter to roll then scoot back to their positions.

        if die_inst.held:
            die_inst.held = False
        else:
            die_inst.held = True

        self.print_updated()
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

export_data = False


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
            import os
            file = rf"{os.getcwd()}\farkle_settings.json"
        return file

    def load_json(self, file_selection):

        file = self.file_select(file_selection)

        import json
        with open(file, "r") as f:
            file_data = json.load(f)

        return file_data

    def output_to_file(self, data, file_selection):

        file = self.file_select(file_selection)

        import json
        with open(file, "w") as f:
            json.dump(data, f, indent=2)


    def start_game(self):

        self.game_data = {self.session_ID: {0: {}}}


    def output_gamedata(self, player, turn = None, end_game=False):

        if not export_data:
            return

        farkle_file = self.load_json("gamedata")

        gamedata = self.game_data.copy()

        if farkle_file:
            for entry in farkle_file:
                if entry and entry != self.session_ID:
                    gamedata[entry] = farkle_file[entry]

        if end_game:
            gamedata[self.session_ID][players.total_games]["game_score"] = {players.current.name: players.current.game_score, players.opponent.name: players.opponent.game_score}

        self.output_to_file(self, gamedata, "gamedata")


    def collect_turndata(self, player:"playerInst", matches=None, die_rolled=None, roll_score=0, bust=False, turn_end=None, game_end=False, initial_roll=False):

        """
            {total_turns}: {
                player: {player.name},
                rolls: [{matches}]
                turn_end_score: {turn_score: game_score}
            }

        """
        write_turn_data = False#True
        force_no_writing = True
        if force_no_writing:
            return

        if die_rolled:
            if not isinstance(die_rolled, list|set|tuple):
                die_rolled = list(die_rolled)

        if initial_roll:
            initial_roll = list(i.value for i in dice.dice)

        if self.turn_data and self.turn_data.get(players.total_turns):
            current_data = self.turn_data[players.total_turns]
        else:
            self.turn_data[players.total_turns] = {"player": player.name, "initial roll": initial_roll, "rolls": {}}
            current_data = self.turn_data[players.total_turns]

        if matches:
            current_data["rolls"][player.roll_count] = ({"Dice": list(i.value for i in die_rolled), "Matches": matches, "Roll score": roll_score})

        if bust:
            current_data["rolls"][player.roll_count] = ({"Dice": list(i.value for i in die_rolled), "Matches": "BUST", "Roll score": roll_score})
            current_data["turn_end_score"] = {0: player.game_score}

        if turn_end:
            current_data["turn_end_score"] = {player.turn_score: player.game_score}
            if write_turn_data:
                self.output_gamedata(player)

        self.game_data.setdefault(self.session_ID, {}).setdefault(players.total_games, {}).setdefault(players.total_turns, current_data)

        if game_end:
            self.output_gamedata(player, end_game=True)

to_json = outputter()

def restore_defaults():

    settings_dict = to_json.load_json("settings")

    for item in settings_dict["defaults"]:
        #print(f"item in default dict: {settings_dict['defaults'][item]} // item: {item}")
        setattr(settings, item, settings_dict["defaults"][item])

    theme_name = settings_dict["defaults"]["game_theme"]
    if "farkle_" in theme_name:
        theme_name = theme_name.replace("farkle_", "")
    sg.theme(f'farkle_{theme_name}')

    settings_dict["user_set"] = {}

    to_json.output_to_file(settings_dict, "settings")

    #print(f"SETTINGS VARS: {vars(settings)}")
    """self.player1_name = settings_dict["defaults"]["player1_name"]
    self.player2_name = settings_dict["defaults"]["player2_name"]
    self.playstyle = settings_dict["defaults"]["playstyle"]
    self.is_singleplayer = settings_dict["defaults"]["is_singleplayer"]
    self.computer_think_aloud = settings_dict["defaults"]["computer_think_aloud"]
    self.output_file = settings_dict["defaults"]["output_file"]"""

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

        self.playstyle = "standard"

    def __repr__(self):
        return f"<player: {self.name} // held_score: {self.held_dice} // turn_score: {self.turn_score}>"

class playerClass:

    def __init__(self):
        self.is_singleplayer = True
        self.default_playstyle = "harpoon"

        self.players:set = set()
        self.player_1 = None
        self.player_2 = None
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

def get_score(player:playerInst=None, autoplay_dice=None, print_result=True, get_score=True, test_only=False): # if print_result, send roll to json
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

    no_playstyle = False#True
    if not no_playstyle:
        if players.is_singleplayer and player.playstyle and (used_dice and len(used_dice) != len(dice_selection)): # only for NPC
            held_score, updated_dice = apply_playstyle(player, held_score, dice_selection)
            if updated_dice:
                used_dice = updated_dice

        to_json.collect_turndata(players.current, matches=matches, die_rolled=dice_selection, roll_score=held_score)

    if not matches and not test_only:
        player.turn_score = 0

    if get_score:
        player.turn_score += held_score
    return held_score, used_dice, print_output

def clear_held_and_used_dice():

    for die in dice.dice:
        die.value = str(die.place_no)
        die.used = False
        die.held = False

def update_tally():

    players.tally[players.total_turns] = (players.current.name, players.current.game_score)
    """count = int(pos.tally)
    column = 4

    for i, entry in players.tally.items():
        name, score = entry
        if count == pos.tally_orig:
            count = int(pos.tally)
            column = column + 32
            if column +30 >= pos.columns:
                column = 4
        print(f"\033[{count};{column}f\033[2;32mTurn {i}: {name} = {score}")
        count = count + 1"""
        #pos.print_error(f"printed tally for {players.current.name} at count {count}, column {column}", 2)
    #print(END, end='')

def held_die_now_used_die(die_inst:die):
    die_inst.used = True
    die_inst.held = False

def mark_used(in_loop):
    for die in in_loop:
        held_die_now_used_die(die_inst=die)

    in_loop.clear()

def take_roll(player:playerInst):

    player.game_score += player.turn_score
    if export_data:
        to_json.collect_turndata(player, turn_end=True)


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
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    """key_inner = key + "_inner"
    if visible:
        collapsable = [
        [sg.VStretch()],
        [sg.Column(layout, key=key_inner, visible=visible, element_justification="center", vertical_alignment="center")],
        [sg.VStretch()]
        ]
    else:
        collapsable =[
            [sg.Column(layout, key=key, visible=visible, element_justification="center", vertical_alignment="center")]]
    return sg.pin(sg.Column(layout=collapsable), vertical_alignment="center")
    """

    return sg.pin(sg.Column(layout, key=key, visible=visible, element_justification="center", vertical_alignment="center", expand_y=True))

def add_dots(dot_size=std_dot_size):
    dot_colour = theme_data.theme_dict[sg.theme()]["dot_colour"]
    dot_instance = sg.Text('•', font=(f"courier {dot_size} bold"), text_color=dot_colour, auto_size_text=True, pad=0, justification="centre")
    return dot_instance

def make_vert_dots(size1=std_dot_size, size2=std_dot_size, size3=std_dot_size):
    return [[add_dots(size1)], [add_dots(size2)], [add_dots(size3)]]

def make_horz_dots(size1=std_dot_size, size2=std_dot_size, size3=std_dot_size):
    return [[add_dots(size1), add_dots(size2), add_dots(size3)]]


def make_window():

    if settings.game_theme == "arcade":
        preroll_cols = { # for farkle_arcade
            "die_1": ("black", "#db270d"),
            "die_2": ("black", "#ffb302"),
            "die_3": ("black", "#71b335"),
            "die_4": ("black", "#4e8f9a"),
            "die_5": ("black", "#4e5b9a"),
            "die_6": ("black", "#ae3aad")
        }
    else:
        preroll_cols = {
            "die_1": ("black", "#B44734"),
            "die_2": ("black", "#D6B72B"),
            "die_3": ("black", "#38B434"),
            "die_4": ("black", "#34A5B4"),
            "die_5": ("black", "#3476B4"),
            "die_6": ("black", "#7A34B4")
        }

    def colour_dice(die_inst=None, preroll = False, do_refresh=False, bust=False):

        def _do_colour(die_inst, do_refresh=False, bust=False):

            dice_place = "die_" + str(die_inst.place_no)
            #window[dice_place].update(button_color="white")
            #sleep(.02)

            if bust:
                window[dice_place].update(bust_text[dice_place])
                window[dice_place].update(button_color=die_bust_col)

            else:
                if preroll:
                    window[dice_place].update(preroll_text[dice_place], button_color="white")
                    window.refresh()
                    sleep(.075)
                    colour = preroll_cols[dice_place]
                    window[dice_place].update(preroll_text[dice_place], button_color=colour)
                    #window[dice_place].update()

                else:
                    if die_inst.held:
                        window[dice_place].update(button_color=button_held)
                    elif die_inst.used:
                        window[dice_place].update(button_color=button_used)
                    else:
                        window[dice_place].update(button_color=players.current.skin)


            if do_refresh:
                window.refresh()
                sleep(die_refresh_val)

        if not die_inst:
            for no in range(1,7):
                _do_colour(dice_dict[f"die_{no}"], do_refresh, bust)

            #for i in dice.dice:
                #_do_colour(i, do_refresh, bust)
        else:
            _do_colour(die_inst, do_refresh, bust)

    def hold_dice(die_inst):

        #dice_place_no = dice_place.replace("die_", '')
        #dice_place_no = int(dice_place_no)
        dice.hold(die_inst)
        colour_dice(die_inst, do_refresh=False)

    def get_die_inst(key):
        key = key.replace("die_", "")
        inst = dice.by_no[int(key)]
        return inst


    def update_die_val_and_colour(new_value, die_inst, do_refresh=True, die_place=None):

        die_inst.value = new_value
        if not die_place:
            die_place = "die_" + str(die_inst.place_no)
        try:
            window[die_place].__setattr__("metadata", str(die_inst.value))
            window[die_place].update(die_inst.value)
            colour_dice(die_inst, do_refresh=do_refresh)
            sleep(die_refresh_val)
        except:
            print()

    def roll_single(die_place_no, die_inst, do_refresh=False):

        if die_inst.held or die_inst.used:
            sleep(.05)
            return

        forced_rolls = {
            #1: [1, 1, 1, 1, 1, 1],
            #1: [1, 1, 1, 2, 3, 2]
            0: [1, 2, 3, 4, 5, 6],
            1: [1, 2, 2, 3, 3, 4]
        }


        if dice.force_dicerolls and forced_rolls.get(players.total_turns):
            for idx, new_value in enumerate(forced_rolls[players.total_turns]):
                if die_inst.place_no == idx+1:
                    update_die_val_and_colour(new_value, die_inst, do_refresh=do_refresh)
                    if idx == 5:
                        dice.force_dicerolls = False
                    return

        update_die_val_and_colour(random.randrange(1,7), die_inst, do_refresh=True, die_place=die_place_no)

    def roll_dice(used_dice=None, do_refresh=False) -> None:


        for i, die_inst in dice_dict.items():
            if used_dice:
                if die_inst in used_dice:
                    continue
                roll_single(i, die_inst, do_refresh=do_refresh)
            else:
                roll_single(i, die_inst, do_refresh=do_refresh)
                #dice.print_updated(die_inst)

    def make_button(width:float=std_btn, height:float=std_btn, key_str:str="Pause", tooltip_str = ''):
        key_upper = key_str.upper()
        key_formatting = str("-" + key_upper + '-')
        #sg.Button("Hello", , use_ttk_buttons=True)
        return sg.Button(key_str, key=key_formatting, mouseover_colors=button_mouseover, use_ttk_buttons=True, size=(width,height), font=(f"courier {std_dot_size} bold"), tooltip=tooltip_str if tooltip_str else None)

    def make_die(key_str:str="1"):

        val = int(key_str.replace("die_", ""))
        text = preroll_text[key_str]
        colour = preroll_cols[key_str]
        #key_upper = str(key_str).upper()
        key_str = key_str#str("die_" + key_upper)
        #sg.Button("Hello", , use_ttk_buttons=True)
        #image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc````\x00\x00\x00\x05\x00\x01\xa5\xf6E@\x00\x00\x00\x00IEND\xaeB`\x82'
        button = sg.Button(button_text=text, button_color=colour, key=key_str, mouseover_colors=button_mouseover, use_ttk_buttons=False, border_width=5, size=(5,2), font=(f"courier 30 bold"), metadata=val)
        dice_dict[key_str] = get_die_inst(key_str)
        return button

    def mid_gap():
        #mid_dots = [[add_dots(std_dot_size)], [add_dots(std_dot_size)]]
        return [[sg.Canvas(size=(12,14))]]


    def round_over(winner:playerInst):
        winner.wins += 1
        clear_held_and_used_dice()
        window["print_player_stats"].update(players.scoreline())#f"Current player: {players.current.name}\nScores: {players.player_1.name}: {players.player_1.game_score} / {players.player_2.name}: {players.player_2.game_score}")

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

            colour_dice(preroll=True, do_refresh=True)
            window["output_line"].update("Starting a new game!")
            window.refresh()

        else:
            window["output_line"].update(f"Thanks for playing! Final scores: {players.player_1.name}: {players.player_1.game_score} points, {players.player_1.wins} games won // {players.player_2.name}: {players.player_2.game_score} points, {players.player_2.wins} games won")
            return "game_over"


    def reset_for_new_turn():
        """Returns "end_game" if not starting a new game, "new_game" if starting a new game."""
        update_tally()
        tally_entries, tally_entries_second = update_tally_entries()
        window["tally_table_P1"].update(tally_entries)
        if tally_entries_second:
            window["tally_table_P2"].update(tally_entries_second, visible=True)
        players.total_turns += 1
        print_output_text(f"{players.current.name} ends their turn with {players.current.turn_score} points, for a total score of {players.current.game_score} points.")
        #print_output_text(f"{print_colour.playernm(players.current, "output")} ends their turn with a score of [[{players.current.game_score}]].")

        players.current.turn_score = 0

        players.current.roll_count = 0
        players.opponent.roll_count = 0

        if players.current.game_score >= points_to_win:
            if round_over(winner=players.current):
                return "end_game"

        players.current, players.opponent = players.opponent, players.current

        clear_held_and_used_dice()

        colour_dice(preroll=True, do_refresh=True)
        window["print_player_stats"].update(players.scoreline())#f"Current player: {players.current.name}\nScores: {players.player_1.name}: {players.player_1.game_score} / {players.player_2.name}: {players.player_2.game_score}")
        to_json.start_game() # do this here so the first turn is always included regardless of PC or human player starting. Could get messy otherwise.


    def print_points_line(score='', bust=False, string_print=''):

        if string_print:
            point_value = string_print
        elif not bust:
            if score:
                point_value = f"Points from this roll: {score} / Current turn score: {players.current.turn_score}"
            else:
                point_value = ''
        else:
            point_value = f"{players.current.name} busts!!"
        window["point_output"].update(point_value)
        return

    def print_output_text(text=''):
        #output_line_str, key="output_line"
        output_line_str = text
        window["output_line"].update(output_line_str)

    def clear_prints():

        print_points_line()
        print_output_text()


    def take_score_and_end_turn(get_turnscore = True):
        clear_prints()
        score = str(players.current.turn_score) # score isn't used anywhere here. remove? #TODO
        if get_turnscore:
            score, _, _ = get_score(players.current, set(i for i in dice.dice if i.held), print_result=True, get_score=True)
        take_roll(players.current)
        outcome = reset_for_new_turn()
        return outcome


    def gui_autoplay(player:playerInst, used_dice):
        """for player_2 to be PC controlled."""

        if not used_dice:
            print_points_line(string_print=f"{players.current.name} is starting their turn.")

        def start_turn():
            print_output_text(text='')
            sleep(.2)
            roll_dice(do_refresh=True)
            to_json.collect_turndata(players.current, die_rolled=dice.dice, initial_roll=True) # only initial if first roll
            #colour_buttons()
            score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice if not i.used), print_result=False, get_score=False)
            sleep(.3)
            if not used_dice:
                return "bust"

        clear_held_and_used_dice()

        while True:

            if start_turn():
                return "bust", None

            unused_dice = set(i for i in dice.dice if not i.used)

            has_potential, used_dice, output_text = get_score(player, unused_dice, print_result=False, get_score=False)

            if not has_potential: # should not get here, as it should get caught by start_turn
                return "bust", None

            for _, inst in dice_dict.items():
                if inst in used_dice:
                    inst.held = True
                    print_output_text(text=output_text)
                    colour_dice(inst, do_refresh=True)
                    sleep(.3)
                print_points_line(has_potential)
                window.refresh()


            score, used_dice, output_text = get_score(player, used_dice)
            for _, inst in dice_dict.items():
                if inst in used_dice:
                    print_output_text(text=output_text)
                    held_die_now_used_die(die_inst=inst)
                    colour_dice(inst, do_refresh=True)
                    sleep(.3)

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
            for _, inst in dice_dict.items():
                if inst in used_dice:
                    print_output_text(text=output_text)
                    colour_dice(inst, do_refresh=True)
                    window.refresh()
                    sleep(.3)

            used_dice_count = sum(1 for d in dice.dice if d.used)

            if (used_dice_count) == 6:
                if (player.game_score + player.turn_score >= points_to_win) or player.turn_score > points_to_win/4:
                    print_output_text(f"{players.current.name} used all their dice and is taking the current score.")
                    window.refresh()
                    return "end_turn", None

                print_output_text(f"{players.current.name} used all their dice; rerolling all.")
                clear_held_and_used_dice()

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
        rules_panel = [[sg.Canvas(size=(widest_measure,2), pad=2)],
                    [sg.Text(text=rules, expand_x=True, expand_y=True, text_color=theme_data().theme_dict[sg.theme()]["gold_text"], justification="center")],
                    [sg.Stretch(), sg.Text(text="[ Note: You can keep the rules open while you play if you like. ]", justification="right")]
                    ]

        rules_main = [[sg.Column(rules_panel)]]

        rules_layout = [[sg.Frame(title="", key="rules_window", layout=rules_main, font=("courier", std_dot_size, "bold"), relief="groove", pad=(5), border_width=5)]]

        #rules_window = sg.Window(' farkle rules ••', rules_layout, enable_close_attempted_event=True, keep_on_top=True, finalize=True, margins=(10,10), alpha_channel=1.0, grab_anywhere=True, no_titlebar=False, use_custom_titlebar=True, titlebar_background_color=theme_data().theme_dict[sg.theme()]["title_bg"], titlebar_text_color=theme_data().theme_dict[sg.theme()]["gold_text"], titlebar_font="courier 10 bold", icon=png_icon)
        rules_window = sg.Window(' rules ••', rules_layout, keep_on_top=True, finalize=True, margins=(10,10), grab_anywhere=True, no_titlebar=False, use_custom_titlebar=True, titlebar_background_color=theme_data().theme_dict[sg.theme()]["title_bg"], titlebar_text_color=theme_data().theme_dict[sg.theme()]["gold_text"], titlebar_font="courier 10 bold", titlebar_icon=png_icon)

        _, _ = rules_window.read(timeout=1000)


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

    settings_rules_and_exit = [[make_button(width=std_btn, height=1, key_str="Settings", tooltip_str = "Change single/two player, player names/colours, theme, etc."), add_dots(), make_button(width=std_btn, height=1, key_str="Rules"), add_dots(), sg.HSeparator(color=gold), add_dots(), make_button(width=std_btn, height=1, key_str="Exit")],
                    [sg.Stretch(), sg.Text(text=players.scoreline(), key="print_player_stats", font=(f"courier {int(std_dot_size) + 2} bold"), text_color=theme_data().theme_dict[sg.theme()]["gold_text"], pad=0, justification="center", size=(60,2)), sg.Stretch()],
                    [sg.Canvas(size=(widest_measure,2))],
                    [sg.HSeparator(color=gold)],
                    [sg.Canvas(size=(widest_measure,2))],
                    [sg.Column(layout=make_vert_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), vertical_alignment="center"),
                     sg.Column(key="dice_layout", layout=dice_display, justification="c", vertical_alignment="center"),
                     sg.Column(layout=make_vert_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), vertical_alignment="center")]]

    text_width = len("points from this roll: 1111 / current turn score: 1111")
    point_output = [
                    [sg.Stretch(), sg.HSeparator(color=gold), sg.Stretch()],
                    [sg.Canvas(size=(widest_measure,2), pad=2)],
                    [sg.Stretch(), sg.Text(point_value, key="point_output", font=(f"courier {int(std_dot_size) + 4} bold"), size=(text_width, 1), pad=0, justification="center"), sg.Stretch()],
                    [sg.Canvas(size=(widest_measure,2), pad=2)],
                    [sg.Stretch(), sg.HSeparator(color=gold), sg.Stretch()]
                    ]

    roll_take_and_output_print =      [
                     [
                     sg.Stretch(), sg.Column(layout=make_horz_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), pad=0),
                     make_button(width=std_btn, height=1, key_str="Roll"), make_button(width=std_btn, height=1, key_str="Take"),
                     sg.Column(layout=make_horz_dots(size1=int(std_dot_size)+4, size2=int(std_dot_size)+2, size3=std_dot_size)),
                     sg.Stretch(),
                     ],

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

    colour_dice(preroll=True)
    round_started = False
    opened1 = False
    window['-SEC1-'].update(visible=False)

    """
    All print lines (in order of appearance):

        window["print_player_stats"].update(f"Current player: {players.current.name}, scores: {players.player_1.name}: {players.player_1.game_score} / {players.player_2.name}: {players.player_2.game_score}")
        print_points_line(string_print='200 points from this roll')
        print_output_text(text=f"{players.current.name} is starting their turn.")

    """

    while True:

        event, values = window.read(timeout=500)

        if event == sg.WIN_CLOSED or event == '-EXIT-' or event == "__TITLEBAR CLOSE__":

            if not window.is_closed():
                clear_prints()
            return "exit", None

        if not window.is_closed(quick_check=False):
            colour_dice(preroll=True if not round_started else False, do_refresh=False if round_started else True)

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
                        clear_print_lines_before_close()
                        window.close()
                        return "exit", None
                        #break

                elif outcome == "bust":
                    print_points_line(bust=True)
                    if check_for_close_event(autoplay_loop_event):
                        return "exit", None
                    colour_dice(do_refresh=True, bust=True)
                    window.refresh()
                    sleep(.5)
                    #colour_buttons(do_refresh=True, bust=True)
                    players.current.turn_score = 0
                    if check_for_close_event(autoplay_loop_event): # added a number of these so it has different opportunities to notice and exit to limit the user wait after clicking close.
                        return "exit", None
                    reset_for_new_turn()
                    round_started = False
                elif outcome == "game_won":
                    round_over(players.current)

        if not round_started:

            autoplay_loop_event, values = window.read(timeout=100)
            clear_held_and_used_dice()
            print_points_line(string_print='')
            print_output_text(text=f"{players.current.name} is starting their turn.")
            sleep(.2)
            if check_for_close_event(autoplay_loop_event):
                return "exit", None
            roll_dice(do_refresh=True)
            to_json.collect_turndata(players.current, die_rolled=dice.dice, initial_roll=True)
            score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice), print_result=False, get_score=False)
            round_started = True
            print_output_text(text=output_str)
            if not used_dice:
                print_points_line(bust=True)
                colour_dice(do_refresh=True, bust=True)
                if check_for_close_event(autoplay_loop_event):
                    return "exit"
                sleep(.8)
                reset_for_new_turn()
                round_started = False

        if event and event.startswith('-OPEN SEC1-'):
            opened1 = not opened1
            window['-OPEN SEC1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_UP)
            window['-SEC1-'].update(visible=opened1)

        if "die_" in event and round_started:
            clear_prints()
            die_inst = get_die_inst(event)
            if die_inst.used:
                continue
            window[event].__getattribute__("metadata")
            hold_dice(die_inst)#, value = window[event].__getattribute__("metadata"))
            score, _, output_str = get_score(players.current, set(i for i in dice.dice if i.held), print_result=False, get_score=False, test_only=True)
            print_output_text(text=output_str)
            print_points_line(score)

        if event == "-ROLL-" and round_started:
            clear_prints()
            held_dice = set(i for i in dice.dice if i.held)
            if not held_dice:
                print_output_text("You must hold at least one die before rolling.")
            else:
                preroll_score, new_used_dice, _ = get_score(players.current, held_dice, print_result=False, get_score=False)
                if preroll_score == 0:
                    print_output_text("You must hold at least one die viable before rolling.")
                    continue

                mark_used(new_used_dice)
                for i in dice.dice:
                    if i.held:
                        i.held=False
                if check_for_close_event(event):
                    return "exit"
                used_dice = set(i for i in dice.dice if i.used)
                if used_dice and len(used_dice) == 6:
                    print_output_text(f"{players.current.name} used all their dice; rerolling all.")
                    clear_held_and_used_dice()
                    #colour_buttons()
                    roll_dice(do_refresh=True)
                else:
                    roll_dice(used_dice, do_refresh=True)
                score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice if not i.used), print_result=False, get_score=False)
                print_output_text(text=output_str)
                if check_for_close_event(event):
                    return "exit"
                if not used_dice:
                    print_points_line(bust=True)
                    colour_dice(do_refresh=True, bust=True)
                    sleep(.8)
                    reset_for_new_turn()
                    round_started = False
                else:
                    players.current.turn_score += preroll_score

        if event == "-TAKE-":
            if not players.current.turn_score and not (dice.dice and any(i.held for i in dice.dice)): # ""any(i.held for i in dice.dice)"" oh so that's a use for any. Good.
                print_output_text("You can't take nothing if there are valid scoring dice.")
                continue
            round_started = take_score_and_end_turn()
            if round_started and round_started == "end_game":
                clear_print_lines_before_close()
                return "exit", None
                break

        if event == "-SETTINGS-":
            clear_prints()
            window.close()
            return None, "use_settings"

        if event == "-RULES-":
            rules_window()

    #TODO
    """if window.get_screen_dimensions() and window.get_screen_dimensions() != (None, None):   #fullscreen version"""

    if not window.is_closed():
        window.close()
    return "exit", None


def settings_window():

    def make_settings_button(width:float=std_btn, height:float=std_btn, key:str="", key_str:str="Pause", tooltip_str=''):
        if key:
            key_formatting = key
        else:
            key_upper = key_str.upper()
            key_formatting = str("-" + key_upper + '-')
        return sg.Button(auto_size_button=True, button_text = key_str, key=key_formatting, mouseover_colors=button_mouseover, use_ttk_buttons=True, size=(width,height), font=(f"courier {std_dot_size} bold"), disabled_button_color = "#756C5F", tooltip=tooltip_str if tooltip_str else None)

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
            #[sg.VStretch()],
            [sg.Column(layout, key=key + "_inner", element_justification="center", background_color=region_3_col, pad=0)],
            #[sg.VStretch()]
            ]
        else:
            collapsable =[
                [sg.Column(layout, key=key + "_inner", element_justification="center", background_color=region_3_col, pad=0)]]
        return sg.pin(sg.Column(layout=collapsable, key=key, visible=visible, justification="center", background_color=region_2_col, pad=0))

        return sg.pin(sg.Column(layout, key=key, visible=visible, element_justification="center", vertical_alignment="center", expand_y=True))

    singleplayer_open = mode_open = names_open = themes_open = False
    blank_open = True

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
                     #[sg.Text(f"The options are: {list(f"[ {i} ]" for i in players.playstyles)}`", justification="center")],
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
                    #[sg.VStretch(background_color="green")],
                    [settings_collapse(blank_settings, "blank"),settings_collapse(singleplayer, '-SEC1-'), settings_collapse(mode, '-MODE-'), settings_collapse(names, '-NAMES-'), settings_collapse(themes, '-THEMES-')],
                    [sg.Canvas(size=(554, 1), background_color=canvas_col, pad=0)]
                    #[sg.VStretch(background_color="green")],
                    #[sg.Stretch(), sg.Canvas(size=(550,2), pad=2), sg.Stretch()],
## Cannot get it to be properly centred no matter what I do. Getting insanely frustrating tbh. Just going to hardcode the placements I think.
    ]

    settings_options = [
                    #[sg.VStretch()],
                    [sg.HSeparator(color=gold)],
                    [
                        make_settings_button(width=std_btn, height=1, key="panel_single_player", key_str="Single player"), add_dots(), sg.HSeparator(color=gold), add_dots(),
                        make_settings_button(width=std_btn, height=1, key="panel_mode", key_str="Computer mode"), add_dots(), sg.HSeparator(color=gold), add_dots(),
                        make_settings_button(width=std_btn, height=1, key="panel_names", key_str="Player names"), add_dots(), sg.HSeparator(color=gold), add_dots(),
                        make_settings_button(width=std_btn, height=1, key="panel_themes", key_str="Colour themes")
                        ],
                    #[sg.VStretch()],
                    [sg.HSeparator(color=gold)],
                    [sg.Column(layout = theme_sections, size=(570, 245), justification="center", element_justification="center", background_color=region_1_col, pad=((4,2),(2,2)))],
                    [sg.HSeparator(color=gold)],
                    #[sg.VStretch()],
                    #[sg.Stretch(), collapse(singleplayer, '-SEC1-'), collapse(mode, '-MODE-'), collapse(names, '-NAMES-'), collapse(themes, '-THEMES-'), sg.Stretch()],
                    [sg.Stretch(), add_dots(), make_settings_button(width=std_btn, height=1, key="leave", key_str="Save changes", tooltip_str="Return to game with the new settings."), add_dots(), make_settings_button(width=std_btn, height=1, key="leave_no_save", key_str="Return without saving", tooltip_str="Closing the settings window without applying changes."), add_dots(), make_settings_button(width=std_btn, height=1, key="restore", key_str="[Restore defaults]", tooltip_str="Restore settings to defaults. Will restart the game."), add_dots(), sg.Stretch()]
                    ]

    settings_main = [
                     [sg.Column(settings_options, justification="center", element_justification="center", pad=5, background_color=region_3_col)]
                    ]

    settings_layout = [[sg.Frame(title=" farkle settings •• ", key="settings_window", layout=settings_main, font=("courier", std_dot_size, "bold"), relief="groove", pad=(5), border_width=5, expand_x=True, element_justification="center")]]

    #settings_window = sg.Window('SETTINGS', settings_layout, keep_on_top=True, finalize=True, alpha_channel=1.0, disable_close=True, grab_anywhere=True, no_titlebar=False, use_custom_titlebar=True, titlebar_background_color="#332b26", titlebar_text_color="#ffd768", titlebar_font="courier 10 bold", titlebar_icon=png_icon)
    settings_window = sg.Window(' settings ••', settings_layout, keep_on_top=True, finalize=True, alpha_channel=1.0, disable_close=False, grab_anywhere=True, no_titlebar=True, use_custom_titlebar=True, titlebar_background_color=theme_data().theme_dict[sg.theme()]["title_bg"], titlebar_text_color=theme_data().theme_dict[sg.theme()]["gold_text"], titlebar_font="courier 10 bold", titlebar_icon=png_icon)
    settings_dict = {}

    settings_window["blank"].update(visible=True)
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
                if event == "panel_single_player":
                    if mode_open:
                        settings_window['-MODE-'].update(visible=False)
                        mode_open = False
                    if names_open:
                        settings_window['-NAMES-'].update(visible=False)
                        names_open = False
                    if themes_open:
                        settings_window['-THEMES-'].update(visible=False)
                        themes_open = False

                    singleplayer_open = not singleplayer_open

                    if singleplayer_open:
                        settings_window['blank'].update(visible=False)

                    settings_window["choose_single"].update(disabled=True if players.is_singleplayer else False)
                    settings_window["choose_two"].update(disabled=False if players.is_singleplayer else True)
                    settings_window['-SEC1-'].update(visible=singleplayer_open)

                    if not singleplayer_open:
                        settings_window['blank'].update(visible=True)

                if event == "panel_mode":
                    if singleplayer_open:
                        settings_window['-SEC1-'].update(visible=False)
                        singleplayer_open = False
                    if names_open:
                        settings_window['-NAMES-'].update(visible=False)
                        names_open = False
                    if themes_open:
                        settings_window['-THEMES-'].update(visible=False)
                        themes_open = False

                    mode_open = not mode_open
                    for style in players.playstyles:
                        settings_window[style].update(disabled=True if players.default_playstyle == style else False)

                    if mode_open:
                        settings_window['blank'].update(visible=False)

                    settings_window['-MODE-'].update(visible=mode_open)

                    if not mode_open:
                        settings_window['blank'].update(visible=True)

                if event == "panel_names":
                    if singleplayer_open:
                        settings_window['-SEC1-'].update(visible=False)
                        singleplayer_open = False
                    if mode_open:
                        settings_window['-MODE-'].update(visible=False)
                        mode_open = False
                    if themes_open:
                        settings_window['-THEMES-'].update(visible=False)
                        themes_open = False

                    names_open = not names_open

                    if names_open:
                        settings_window['blank'].update(visible=False)

                    settings_window['-NAMES-'].update(visible=names_open)

                    if not names_open:
                        settings_window['blank'].update(visible=True)

                if event == "panel_themes":
                    if singleplayer_open:
                        settings_window['-SEC1-'].update(visible=False)
                        singleplayer_open = False
                    if mode_open:
                        settings_window['-MODE-'].update(visible=False)
                        mode_open = False
                    if names_open:
                        settings_window['-NAMES-'].update(visible=False)
                        names_open = False

                    themes_open = not themes_open
                    if themes_open:
                        settings_window["choose_tan"].update(disabled=True if "tan" in sg.theme() else False)
                        settings_window["choose_navy"].update(disabled=True if "navy" in sg.theme() else False)
                        settings_window["choose_arcade"].update(disabled=True if "arcade" in sg.theme() else False)
                        settings_window['blank'].update(visible=False)

                    settings_window['-THEMES-'].update(visible=themes_open)

                    if not themes_open:
                        settings_window['blank'].update(visible=True)

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
                return "no_save" # just here while I'm forcing settings window, remove after.


def update_json(update_data:dict):

    """updates JSON with provided dict. Only the keys provided will be updated, and only if the value is different to the current value."""
    json_data = to_json.load_json("settings")
    for key, value in update_data.items():
        json_data["user_set"][key] = value

    to_json.output_to_file(json_data, "settings")


def apply_settings(settings_dict):
    """applies settings to relevant game vars/classes, and updates JSON if enabled and necessary."""
    update_json_dict = {}

    for action, data in settings_dict.items():

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
            #print(f"DATA for change names: {data}")
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
                        if "colour: " in colour:
                            colour = colour.split("colour: ")[1]
                        if player_num == "1":
                            if players.player_1.skin != colour:
                                players.player_1.skin = colour
                                update_json_dict["player1_col"] = data[name]
                        elif player_num == "2":
                            if players.player_2.skin != colour:
                                players.player_2.skin = colour
                                update_json_dict["player2_col"] = data[name]

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
        update_json(update_json_dict)


def main_gui():

    init_settings()

    make_play_area() # needed for pos initialisation.

    global players
    players = playerClass()

    init_classes(player1 = settings.player1_name, player2 = settings.player2_name, player1_col = settings.player1_col, player2_col = settings.player2_col)

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
                if settings_dict and not isinstance(settings_dict, str): # added this in case I forget to remove the no_save line from settings window testing.
                    apply_settings(settings_dict)

main_gui()

