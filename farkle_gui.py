"""simple text-based farkle game
started April 2026 //  [gui version] v 1.1 // harpoonlobotomy"""

# have commented out to_json throughout, add it back later.
from time import sleep
from typing import Literal
#from typing import Literal


global used_dice
used_dice = set()

def make_play_area():

    import os
    os.system("cls")

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


def get_input():
    pos.print_input(">> ")
    #print(SHOW, end='')
    test = input()
    #print(HIDE, end='')
    pos.print_input("     ") # to clear the line once input is accepted.
    return test

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
        self.held_dice:set[die] = set()


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


    def apply_playstyle(self, player:"playerInst", turn_score, available_dice:set["die"]):

        think_aloud = True

        playstyle_rules = {

            "harpoon": {
                "take_risk": {
                    "I'm over 2000 points behind": (players.opponent.game_score - 2000) > player.game_score,
                    "My opponent too close to winning": players.opponent.game_score > 3200,
                    "I don't have enough score from this roll": player.turn_score + turn_score < 500
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
                pos.print_prompt(f"I'll reroll the rest; {risk_reason}")
                sleep(0.5)
            #print(f"USE DICE: {use_dice}")
            return turn_score, use_dice

        return turn_score, None


    def roll(self):

        forced_rolls = {
            #1: [1, 1, 1, 1, 1, 1],
            1: [1, 1, 1, 2, 3, 2],
            2: [1, 1, 1, 4, 5, 6],
            3: [3, 3, 3, 6, 6, 5],
            4: [1, 2, 3, 4, 5, 6],
            5: [5, 5, 5, 5, 5, 5]
        }

        force_dicerolls = False#True
        if force_dicerolls and forced_rolls.get(players.total_turns):
            for idx, i in enumerate(forced_rolls[players.total_turns]):
                for die in self.dice:
                    if die.place_no == idx+1:
                        die.value = i
                        sleep(0.015)
                        self.print_updated(die)
                        print()
                    sleep(0.01)

        else:
            import random
            count = 0
            for die in self.dice:
                self.print_updated(die)
            while count < 4:
                print(pos.dice_line.replace("7f", f"{pos.dice_pos.get(1)}f"))
                for die in self.dice:
                    if not die.held and not die.used:
                        die.value = random.randint(1, 6)
                        sleep(0.015)
                        self.print_updated(die)
                        print()
                    sleep(0.01)

                self.print_updated()
                count += 1
        sleep(0.1)


    def hold(self, die_inst): # selecting by place_no; if there was a graphic, they would scatter to roll then scoot back to their positions.

        if die_inst.held:
            die_inst.held = False
            dice.held_dice.remove(die_inst)
            #player.held_score -= die.value
            #self.hold_formatting(die)
        else:
            die_inst.held = True
            #player.held_score += die.value
            dice.held_dice.add(die_inst)
            #self.hold_formatting(die)
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

    def start_game(self):

        self.game_data = {self.session_ID: {0: {}}}


    def output_gamedata(self, player, turn = None, end_game=False):

        if not export_data:
            return

        import json
        file = r"D:\Git_Repos\farkle\farkle.json"

        with open(file, "r") as f:
            farkle_file = json.load(f)

        gamedata = self.game_data.copy()

        if farkle_file:
            for entry in farkle_file:
                if entry and entry != self.session_ID:
                    gamedata[entry] = farkle_file[entry]

        if end_game:
            gamedata[self.session_ID][players.total_games]["game_score"] = {players.current.name: players.current.game_score, players.opponent.name: players.opponent.game_score}

        with open(file, "w") as f:
            json.dump(gamedata, f, indent=2)


    def collect_turndata(self, player:"playerInst", matches=None, die_rolled=None, roll_score=0, bust=False, turn_end=None, game_end=False, initial_roll=False):

        """
            {total_turns}: {
                player: {player.name},
                rolls: [{matches}]
                turn_end_score: {turn_score: game_score}
            }

        """
        write_turn_data = False#True
        force_no_writing = False
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

def clear_screen(limited=False):

    #sleep(.3)
    print("\033[1;1H", end='')
    for i in range(pos.lines):
        if limited == True:
            if f"[{i-1};" in pos.output_line:
                break

        print("\033[K")
        sleep(0.03)
        print(end='')

    if not limited:
        import os
        os.system("cls")
    #pos.print_dice(text=" "* len(positions))
    sleep(.15)

class playerClass:

    def __init__(self):
        self.is_singleplayer = False
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

    def __repr__(self):
        return f"Players: {self.players} Current player: {self.current.name}"

    def switch_players(self):
        self.current, self.opponent = self.opponent, self.current
        sleep(1.5)
        clear_screen(limited=True)
        sleep(.3)
        pos.print_output(f"Switching players, next up is {print_colour.playernm(players.current, "output")}...")
        print()
        sleep(1.8)


def init_classes(player1 = "player_1", player2 = "player_2", player1_col = "red", player2_col = "blue"):

    if players.players:
        players.players = set() # clear existing players if any (for resetting names, single-player etc.)

    if players.is_singleplayer:
        player2 = players.default_playstyle
        print(f"Player 2 name: `{player2}`")

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

            #import random
            #player_2.playstyle = random.choice(players.playstyles)

    return dict({"player_1": player_1, "player_2": player_2})

def get_dice_by_val(i, val, player, in_loop:set[die]):
    #print(f"val in test.split: {val}")
    for i in range(1, 7):
        inst  = dice.by_no.get(i)
        #print(f"item: {i} // inst: {inst}")
        if inst.value == int(val) and inst not in in_loop and not inst.used:
            val = i
            #print(f"(Holding die in position [{val}])")
            dice.hold(inst)#players.get(player) if player_1 else players.get("player_2"))
            in_loop.add(inst)
            return in_loop
        #elif inst.value == int(val) and inst in in_loop:
            #print(f"(Already held die with value {val} in this turn, skipping.)")
    return in_loop


def get_score(player:playerInst=None, autoplay_dice=None, print_result=True, get_score=True, test_only=False): # if print_result, send roll to json
    """returns held_score (int) and used_dice (set)"""
    if autoplay_dice:
        dice_selection = set(autoplay_dice)
    else:
        dice_selection = dice.held_dice # Not used anymore, will remove later.

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
            #pos.print_error(f"matched 1-5")
#        if (all("1", "2", "3", "4", "5") in vals):
        #else:
            matched = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            #if matched:
                #pos.print_error(f"matched 2-6")
        if matched and len(matched) == 5:
            #used_dice.update(set(i for i in dice_selection if len(used_dice) < 5 and i.value in vals and i not in used_dice))#(2, 3, 4, 5, 6) if i in vals)#die for die in dice_selection if die.value == item and die not in used_dice)
        #elif (all("2", "3", "4", "5", "6") in vals):
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
        if player and player.playstyle and (used_dice and len(used_dice) != len(dice_selection)): # only for NPC
            held_score, updated_dice = dice.apply_playstyle(player, held_score, dice_selection)
            if updated_dice:
                used_dice = updated_dice

    if print_result and held_score:
        print_output = f"{print_colour.playernm(player, "output")} can score [[{held_score}]] points here if they choose to take the points, taking their total score to [[{player.game_score + player.turn_score + held_score}]]."
        pos.print_output(f"{print_colour.playernm(player, "output")} can score [[{held_score}]] points here if they choose to take the points, taking their total score to [[{player.game_score + player.turn_score + held_score}]].")
        #.collect_turndata(players.current, matches=matches, die_rolled=dice_selection, roll_score=held_score)

    if not matches and not test_only:
        player.turn_score = 0
        #to_json.collect_turndata(players.current, die_rolled=dice_selection, roll_score=held_score, bust=True)
        print_output = f"BUST! Ending {players.current.name}'s turn."
        pos.print_output(f"BUST! Ending {players.current.name}'s turn.")
        print()
        sleep(.8)

    if get_score:
        player.turn_score += held_score
    return held_score, used_dice, print_output

def clear_held_and_used():

    for die in dice.dice:
        die.value = str(die.place_no)
        die.used = False
        die.held = False
        if die in dice.held_dice:
            dice.held_dice.remove(die)

def round_over(winner:playerInst):

    sleep(1.5)
    clear_screen(limited=True)
    sleep(.3)
    pos.print_output(f"Round over! {winner.name} wins with a score of {winner.game_score}!")
    print()
    sleep(1.8)

    winner.wins += 1
    players.opponent.losses += 1
    to_json.collect_turndata(player=winner, game_end=True)
    players.total_games += 1
    clear_held_and_used()
    for player in (winner, players.opponent):
        player.game_score = 0
        player.turn_score = 0
        player.turn_count = 0
    players.total_turns = 0

    players.tally = {}
    clear_screen()
    return

def update_tally():

    players.tally[players.total_turns] = (players.current.name, players.current.game_score)
    count = int(pos.tally)
    column = 4

    for i, entry in players.tally.items():
        name, score = entry
        if count == pos.tally_orig:
            count = int(pos.tally)
            column = column + 32
            if column +30 >= pos.columns:
                column = 4
        print(f"\033[{count};{column}f\033[2;32mTurn {i}: {name} = {score}")
        count = count + 1
        #pos.print_error(f"printed tally for {players.current.name} at count {count}, column {column}", 2)
    #print(END, end='')


def end_turn(player:playerInst):
    pos.print_prompt(clear=True)
    sleep(.05)
    print("\033[1;37m")
    pos.print_output(f"{print_colour.playernm(player, "output")} ends their turn with a score of [[{player.game_score}]].")
    sleep(.8)
    print()
    clear_held_and_used()
    players.current.roll_count = 0
    players.opponent.roll_count = 0

    if player.game_score >= 4000:
        round_over(winner=player)
        return "end_turn"

    player.turn_score = 0
    return

def mark_used(in_loop):
    for die in in_loop:
        die.used = True
        die.held = False

    in_loop.clear()

def do_roll():

    #used = list(i for i in dice.dice if i.used)
    #if used and len(used) == 6: #NOTE: Not working properly yet.
        #pos.print_output("All dice used, resetting for next roll.")
        #for die in used:
            #die.used = False
    dice.roll()
    players.current.roll_count += 1

def take_roll(player:playerInst):

    player.game_score += player.turn_score
    if export_data:
        to_json.collect_turndata(player, turn_end=True)
    if end_turn(player):
        return "game over"


"""def play_turn(player:playerInst):

    if player.skin:
        dice.skin = player.skin
    else:
        dice.skin = ""
    player.turn_count += 1
    pos.print_output(f"{print_colour.playernm(player, "output")} is rolling...")
    dice.set_default_val()
    dice.print_updated()
    dice.roll()
    to_json.collect_turndata(player, initial_roll=True)


    #turn_score = int used holding the score of a single turn,  without considering past turns in this game.
    #game_score = int used for holding player score for the current game, adding each turn_score when the held dice are added.

    in_loop = set()
    reserved = 0
    while True:
        if players.autoplay and ((isinstance(players.autoplay, playerInst) and player == players.autoplay) or isinstance(players.autoplay, bool)):
            return autoplay(player)

        #has_potential, _ = dice.auto_best(output_results=False)
        die_set = in_loop if in_loop else set(i for i in dice.dice if not i.used)
        #input(f"\n\n\ndie set: {die_set}")
        has_potential, _, _ = get_score(player, autoplay_dice=die_set, print_result=True if in_loop else False, get_score=False)
        #pos.print_error(f"HAS POTENTIAL: {has_potential}")
        if not has_potential:
            clear_held_and_used()
            return

        if in_loop:
            pos.print_prompt("Enter more values to add to the selection, or hit enter to take the selected dice.")
        else:
            pos.print_prompt("Enter the values of the dice you want to hold.")

        test = get_input()
        #pos.print_input(f"        >> {SHOW}")
        pos.print_prompt(clear=True)
        if (test or not in_loop) and not len(dice.held_dice) == 6:
            #input("\n\n\n\n\n\ntest or not in_loop (hit enter)")
            while test.lower() in ("take", "roll", "t", "r"):
                test = get_input()
                #pos.print_input(f"        >> {SHOW}")

            test = test.replace(" ", "")
            for i, val in enumerate(list(test)):
            #for i, val in enumerate(test.strip().split(" ")):
                if not val or val not in ("1", "2", "3", "4", "5", "6"):
                    continue
                try:
                    in_loop = get_dice_by_val(i, val, player, in_loop)
                except ValueError as e:
                    pos.print_error(e)
            dice.print_updated()

        else:
            pos.print_output(f"Getting score...")

            #has_potential, in_loop = dice.auto_best(output_results=True, is_auto=False)
            score, _, _ = get_score(player, in_loop)

            mark_used(in_loop)

            dice.print_updated()

            if len(dice.held_dice) == 6:
                pos.print_prompt("All dice used. Do you want to [reroll] or [take] the current score? (Enter 'reroll' or 'take')")
                #pos.print_input(f"        >> {SHOW}")
                test = get_input()

                if test.lower() in ["reroll", "roll", "r"]:
                    reserved = reserved + score
                    clear_held_and_used()
                    do_roll()
                else:
                    return take_roll(player)

            else:
                while True:
                    pos.print_prompt(f"Do you want to take the points, or continue rolling? (enter `take` or `roll`; defaults to `take` if left blank.)")
                    test = get_input()
                    #pos.print_input(f"        >> {SHOW}")
                    if (test.lower() in ("take", "t", "1")) or not test:
                        return take_roll(player)

                    elif test.lower() in ("roll", "r", "2"):
                        do_roll()
                        break
                    else:
                        pos.print_error("Invalid input, please enter `take` or `roll`.")"""

def print_wins():
    sleep(.3)
    pos.print_points(f"{print_colour.playernm(players.current, "points")} has won {players.current.wins} game(s).  {print_colour.playernm(players.opponent, "points")} has won {players.opponent.wins} game(s).")
    print()
    sleep(.8)


def pick_player_names(name_1='', name_2=''):


    pick_names = True if not (name_1 and name_2) else False

    player1 = "player_1"
    player2 = "player_2"

    check_names = False

    if pick_names:
        while True:
            pos.print_prompt("Enter the name for Player 1: ")
            player1 = get_input()

            if not player1:
                pos.print_output(f"Defaulting to `{player1}`. Press 'enter'")
                input()
                pos.print_output(" ",  clear=True)
                player1 = "player_1"
                break
            else:
                if check_names:
                    pos.print_prompt(f"Is this correct? `{player1}`")
                    test = get_input()
                    if (test and test.lower() in ("y", "yes")) or not test:
                        break
                else:
                    break

        if not players.is_singleplayer:
            while True:
                pos.print_prompt("Enter the name for Player 2: ")
                player2 = get_input()

                if not player2:
                    pos.print_output(f"Defaulting to `{player2}`. Press 'enter'")
                    input()
                    pos.print_output(" ", clear=True)
                    player2 = "player_2"
                    break
                else:
                    if check_names:
                        pos.print_prompt(f"Is this correct? `{player2}`")
                        test = get_input()
                        if (test and test.lower() in ("y", "yes")) or not test:
                            break

    init_classes(player1, player2, player1_col = "blue", player2_col = "red")

    if players.is_singleplayer:
        while True:
            #not_choose_playstyle = True
            #if not_choose_playstyle:
            #    players.autoplay.playstyle = "harpoon" # hardset to this model
            players.autoplay.playstyle = players.default_playstyle

            pos.print_prompt(clear=True)
            #pos.print_prompt(f"Computer is set to `{players.autoplay.playstyle}` mode. Type `settings` to change mode, or press enter to continue.")
            #test = get_input()
            test = ''
            pos.print_output(" ", clear=True)
            if test and test == "settings":
                sleep(.2)
                names = [f"[ {i} ]  " for i in players.playstyles]
                pos.print_prompt(f"Please choose a PC player-type: {''.join(names)}")
                pos.print_output(f"'Standard' just takes the best dice available without strategy. 'Harpoon' is the author.")

                chosen = get_input()
                if not chosen:
                    pos.print_output("Keeping current playstyle.")

                elif chosen.strip().lower() in players.playstyles:
                    players.autoplay.playstyle = chosen
                    pos.print_output(f"Mode set to `{players.autoplay.playstyle}`.")

                else:
                    pos.print_output(f"`{chosen}` is not a valid playstyle. Keeping existing playstyle.")
                print()
                #sleep(.8)
            players.autoplay.name = players.autoplay.playstyle

            break


    return player1, player2

def print_rules():
    clear_screen()
    rules = "SCORING: \n\nA `straight` (`1, 2, 3, 4, 5, 6`) is 1500 points\nA `small straight` (either `1, 2, 3, 4, 5` or `2, 3, 4, 5, 6`) is 750 points\n" \
    "Three-of-a-kind is `number x 100` (eg `3, 3, 3` is 300 points.)\nFour of a kind is `2x (number x 100)` (eg `3, 3, 3, 3` is 600 points)\n\n" \
    "1's and 5's are special: All other numbers are only valuable as part of one of the combinations above, and cannot be chosen alone.\n" \
    "But -- a `1` on its own is worth 100 points, and a `5` on its own is worth 50 points. \n\n" \
    "* 1's are extra special: instead of 'number x 100', they are 'number x 1000' ie, `1, 1, 1, 1` is 2000 points.\n\n" \
    "You must select at least one die each roll. If there is no valid die to select, you will bust, ending your turn and losing your points from that turn.\n" \
    "After selecting one or more die, you can choose to keep the points from those dice, or reroll the dice left over to try to get more points.\n\n" \
    "First player to 4000 points wins!\n\n[Press any key to return to Farkle.]"
    pos.print_points(rules, delay=True)
    input()
    clear_screen()

"""def do_turns():
        pos.print_points(f"Current turn: {players.total_turns + 1}  Current player: {print_colour.playernm(players.current, "points")}.\n{print_colour.playernm(players.current, "points")} has {players.current.game_score} points. {print_colour.playernm(players.opponent, "points")} has {players.opponent.game_score} points.")
        sleep(0.2)
        dice.set_default_val()
        sleep(.5)
        players.total_turns += 1
        if play_turn(players.current):
            print_wins()

            pos.print_prompt("Do you want to play again?")
            if players.autoplay and isinstance(players.autoplay, bool): # only autoplay next round if both players are PC
                test = "yes"
            else:
                test = get_input()

            if (test and ("n" in test.lower() or "no" in test.lower())) or not test:
                pos.print_output("Alright, goodbye!")
                print("\n\n\n\n")
                return "end"
        else:
            update_tally()
        players.switch_players()"""

def main():

    global to_json
    to_json = outputter()

    print(HIDE)
    make_play_area()

    pos.print_prompt("Do you want to read the rules?")
    test = get_input()
    if test and test.lower() in ("y", "yes"):
        print_rules()


    pos.print_prompt("How many human players? Enter '1' or '2'.")

    while True:
        test = get_input()

        if (test and "1" in test or "2" in test) or not test:
            if not test or "1" in test:
                if not test:
                    pos.print_output(f"Defaulting to one human, one computer. Press 'enter'")
                    input()
                    pos.print_output(" ",  clear=True)
                single_player = True
            else:
                single_player = False
            break


    pick_player_names("Player_1", "Player_2")


    print()
    sleep(.2)
    import os
    os.system("cls")
    print()
    sleep(.2)
    while True:
        if do_turns():
            break
        #pos.print_points(f"{print_colour.playernm(players.current, "points")} has won {players.current.wins} game(s).  {print_colour.playernm(players.opponent, "points")} has won {players.opponent.wins} game(s).")

#### GUI ####

#https://github.com/PySimpleGUI/PySimpleGUI/issues/4909 <- change button bg col and button mouseover col.

import FreeSimpleGUI as sg
eggplant = "#3E2857",
navy = "#284157"
ivory = "#E0DAC5"
farkle_navy = {'BACKGROUND': navy,
                'TEXT': "#25775f",
                'INPUT': "#45523F",
                'TEXT_INPUT': "#f5db74",
                'SCROLL': "#003e9b",
                'BUTTON': ('black', "#F8DC5E"),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 3,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}
farkle_tan = {'BACKGROUND': ivory,
                'TEXT': "#25775f",
                'INPUT': "#45523F",
                'TEXT_INPUT': "#f5db74",
                'SCROLL': "#003e9b",
                'BUTTON': ('black', "#F8DC5E"),
                'PROGRESS': ('#01826B', '#D0D0D0'),
                'BORDER': 3,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}



sg.theme_add_new('farkle_tan', farkle_tan)
sg.theme_add_new('farkle_navy', farkle_navy)
sg.theme('farkle_tan')

std_dot_size=10
widest_measure = 340
half_measure = (widest_measure/2)-5
std_btn = 10
num_pad_w = 20
num_pad_h = 8
numbers_size = 40
border_lg = 6
five = 5
two = 2
size_text="small"
small_hide=False
tooltip_str="Press to change to small version"
restart_str="[Restart]"
pause_str="[Paused]"

bg_brown="#332b26"
bg_blue = "#36554E"#"darkblue"
numbers_colour="yellow"
dot_colour = "#332b26"
button_mouseover="#105C26"
button_held = "#F8DC5E"
button_used = "#666354"
button_std = ('black', "#5AC280")
player_2_die = ('black', "#5A90C2")

die_bust_col = ('white', "#330303")

icon_str = None
dice_dict = {}

die_1 = 1
die_2 = 2
die_3 = 3
die_4 = 4
die_5 = 5
die_6 = 6

used_dice = dice.dice

point_value = ''
output_line_str = ''

SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'

def collapse(layout, key, visible=False):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=visible))

def add_dots(dot_size=std_dot_size):
    dot_instance = sg.Text('•', font=(f"courier {dot_size} bold"), text_color=dot_colour, auto_size_text=True, pad=0, justification="centre")
    return dot_instance

def make_vert_dots(size1=std_dot_size, size2=std_dot_size, size3=std_dot_size):
    return [[add_dots(size1)], [add_dots(size2)], [add_dots(size3)]]

def make_horz_dots(size1=std_dot_size, size2=std_dot_size, size3=std_dot_size):
    return [[add_dots(size1), add_dots(size2), add_dots(size3)]]


def make_window():

    preroll_cols = {
        "die_1": ("black", "#B44734"),
        "die_2": ("black", "#D6B72B"),
        "die_3": ("black", "#38B434"),
        "die_4": ("black", "#34A5B4"),
        "die_5": ("black", "#3476B4"),
        "die_6": ("black", "#7A34B4")
    }

    def colour_buttons(die_inst=None, preroll = False, do_refresh=False, bust=False):

        def _do_colour(die_inst, do_refresh=False, bust=False):

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

            dice_place = "die_" + str(die_inst.place_no)

            if bust:
                window[dice_place].update(bust_text[dice_place])
                window[dice_place].update(button_color=die_bust_col)

            else:
                if preroll:
                    colour = preroll_cols[dice_place]
                    window[dice_place].update(preroll_text[dice_place], button_color=colour)
                    #window[dice_place].update()

                else:
                    if die_inst.held:
                        window[dice_place].update(button_color=button_held)
                    elif die_inst.used:
                        window[dice_place].update(button_color=button_used)
                    else:
                        if players.current == players.player_2:
                            window[dice_place].update(button_color=player_2_die)
                        else:
                            window[dice_place].update(button_color=button_std)

            if do_refresh:
                window.refresh()
                sleep(.2)

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
        colour_buttons(die_inst, do_refresh=False)

    def identify_die(key_str):
        if key_str == "die_1":
            val = die_1
        if key_str == "die_2":
            val = die_2
        if key_str == "die_3":
            val = die_3
        if key_str == "die_4":
            val = die_4
        if key_str == "die_5":
            val = die_5
        if key_str == "die_6":
            val = die_6
        return val

    def get_die_inst(key):
        key = key.replace("die_", "")
        inst = dice.by_no[int(key)]
        return inst

    def get_die_val(key_str):
        val = identify_die(key_str)
        return val

    def roll_single(i, die_inst, do_refresh=False):
        import random
        if not die_inst.held and not die_inst.used:
            die_inst.value = random.randrange(1,7)
        #print(f"VALUES FOR EVENT {i}:")
        #print(f"VALUE: {die.ButtonText}")
        window[i].__setattr__("metadata", str(die_inst.value))
        #window[i].__setattr__("button_text", str(roll_outcome))
        #sset_die_val(i, roll_outcome)
        window[i].update(die_inst.value)
        colour_buttons(die_inst, do_refresh=do_refresh)

    def roll_dice(do_refresh=False):

        for i, die_inst in dice_dict.items():
            roll_single(i, die_inst, do_refresh=do_refresh)
                #dice.print_updated(die_inst)

    def make_button(width:float=std_btn, height:float=std_btn, key_str:str="Pause", tooltip_str = ''):
        key_upper = key_str.upper()
        key_formatting = str("-" + key_upper + '-')
        #sg.Button("Hello", , use_ttk_buttons=True)
        return sg.Button(key_str, key=key_formatting, mouseover_colors=button_mouseover, use_ttk_buttons=True, size=(width,height), font=(f"courier {std_dot_size} bold"), tooltip=tooltip_str)

    def make_die(key_str:str="1"):

        val = get_die_val(key_str)

        #key_upper = str(key_str).upper()
        key_str = key_str#str("die_" + key_upper)
        #sg.Button("Hello", , use_ttk_buttons=True)
        image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc````\x00\x00\x00\x05\x00\x01\xa5\xf6E@\x00\x00\x00\x00IEND\xaeB`\x82'
        button = sg.Button(button_text=str(val), button_color=button_std, key=key_str, mouseover_colors=button_mouseover, use_ttk_buttons=False, border_width=5, size=(5,2), font=(f"courier 30 bold"), metadata=val)
        dice_dict[key_str] = get_die_inst(key_str)
        return button

    def mid_gap():
        #mid_dots = [[add_dots(std_dot_size)], [add_dots(std_dot_size)]]
        return [[sg.Canvas(size=(12,14))]]

    def reset_for_new_turn():
        update_output_line(f"{players.current.name} ends their turn with a score of {players.current.game_score} points.")
        #update_output_line(f"{print_colour.playernm(players.current, "output")} ends their turn with a score of [[{players.current.game_score}]].")
        end_turn(players.current)

        players.current, players.opponent = players.opponent, players.current

        clear_held_and_used()

        #for die_inst in dice.dice:
            #window[f"die_{str(die_inst.place_no)}"].update(str(die_inst.value))
        colour_buttons(preroll=True, do_refresh=True)

    def write_points(score='', bust=False, string_print=''):

        if string_print:
            point_value = string_print
        elif not bust:
            if score:
                point_value = f"Points from this roll: {score}"
            else:
                point_value = ''
        else:
            point_value = f"{players.current.name} busts!!"
        window["point_output"].update(point_value)

        return

    def update_output_line(text=''):
        #output_line_str, key="output_line"
        output_line_str = text
        window["output_line"].update(output_line_str)

    def clear_prints():
        write_points()
        update_output_line()

    def take_score_and_end_turn(get_turnscore = True) -> Literal[False]:
        clear_prints()
        print(f"take_score starting turn_score: {players.current.turn_score}, game_score: {players.current.game_score}")
        if get_turnscore:
            score, _, _ = get_score(players.current, set(i for i in dice.dice if i.held), print_result=True, get_score=True)
        print(f"take_score starting turn_score: {players.current.turn_score}")
        take_roll(players.current)
        print(f"\nafter take_roll starting turn_score: {players.current.turn_score}, game_score: {players.current.game_score}")
        reset_for_new_turn()
        #round_started = False
        return False

    def game_won(player):

        write_points(string_print=f"{player.name} has won with {player.game_points}!")

        for p in players.players:
            p.game_score = 0
            p.turn_count = 0

    def gui_autoplay(player:playerInst, used_dice):
        """for player_2 to be PC controlled."""

        if not used_dice:
            write_points(string_print=f"{players.current.name} is starting their turn.")

        def start_turn():
            update_output_line(text='')
            sleep(.2)
            roll_dice(do_refresh=True)
            #colour_buttons()
            score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice if not i.used), print_result=False, get_score=False)
            update_output_line(text=output_str)
            sleep(.5)
            if not used_dice:
                return "bust"

        clear_held_and_used()

        while True:

            if start_turn():
                return "bust", None

            unused_dice = set(i for i in dice.dice if not i.used)

            has_potential, used_dice, output_text = get_score(player, unused_dice, print_result=False, get_score=False)


            #has_potential, used_dice = dice.auto_best(player)
            #pos.print_error(f"HAS POTENTIAL: {has_potential}")# USED DICE: {used_dice}")
            #has_potential = dice.dice_potential(starting=True)
            if not has_potential:
                colour_buttons(do_refresh=True, bust=True)
                #player.game_score = 0#+= player.turn_score
                return "bust", None
                #return end_turn(player)

            for i in used_dice:
                i.held = True
                colour_buttons(i, do_refresh=True)

            score, used_dice, _ = get_score(player, used_dice)

            mark_used(used_dice)

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

            colour_buttons(do_refresh=True)

            used_dice_count = sum(1 for d in dice.dice if d.used)

            if (used_dice_count) == 6:
                if player.game_score + player.turn_score >= 4000:
                    pos.print_prompt("All dice used. Taking current score.")
                    return "game_won", None
                pos.print_prompt("All dice used. Rolling again.")
                clear_held_and_used()

            else:
                if (used_dice_count < 4 and (player.game_score + player.turn_score < 4000)) or player.turn_score < 500:
                    pos.print_prompt("Rolling again.")
                    #pos.print_output("Roll done, checking for potential...")
                else:
                    pos.print_prompt(f"{player} ends their turn with {player.turn_score} points.")
                    return "end_turn", None
                    #return take_roll(player)

    dice_display = [[make_die("die_1"),#counter_text("die_1", None, 1),
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

    tally_board = [[sg.VStretch(), sg.Table(values = [[1]], key="tally_table_P1", display_row_numbers=True, starting_row_number=1, headings=[f"{players.current.name}"], expand_x=True, hide_vertical_scroll=True, def_col_width = 40, auto_size_columns=False), sg.Table(values = [[1]], key="tally_table_P2", display_row_numbers=True, starting_row_number=1, headings=[f"{players.opponent.name}"], expand_x=True, hide_vertical_scroll=True, def_col_width = 40, auto_size_columns=False)]]

    column_one_vert = [[make_button(width=std_btn, height=1, key_str="Settings", tooltip_str = "NOTE: Opening 'settings' will end the current game."), add_dots(), sg.HSeparator(color="gold"), add_dots(), make_button(width=std_btn, height=1, key_str="Exit")],
                       [sg.Canvas(size=(widest_measure,two))],
                    [sg.Column(layout=make_vert_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), vertical_alignment="center"),
                     sg.Column(key="dice_layout", layout=dice_display, justification="c", vertical_alignment="center"),
                     sg.Column(layout=make_vert_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), vertical_alignment="center")]]

    column_two_vert = [[sg.Canvas(size=(widest_measure,two), pad=two)],
                    [sg.HSeparator(color="gold")],
                    #[sg.Canvas(size=(widest_measure,five))],
                    [sg.Canvas(size=(widest_measure,two), pad=two)],
                     #sg.InputText(default_text='', size=(int(std_dot_size)+6, int(std_dot_size)*2), border_width=two, focus=False, enable_events=True, justification="c", font=("courier", std_dot_size, "bold"),
                     #   key='-INPUT-', tooltip="Enter the dice values you wish to hold."),
                     [sg.VStretch()],
                     [
                     sg.Stretch(),
                     sg.Column(layout=make_horz_dots(size1=std_dot_size, size2=int(std_dot_size)+2, size3=int(std_dot_size)+4), pad=0),
                     sg.Stretch(), make_button(width=std_btn, height=1, key_str="Roll"), sg.Stretch(), make_button(width=std_btn, height=1, key_str="Take"),
                     sg.Column(layout=make_horz_dots(size1=int(std_dot_size)+4, size2=int(std_dot_size)+2, size3=std_dot_size)),
                     sg.Stretch()
                     ],
                     [sg.VStretch()],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [sg.HSeparator(color="gold")],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],

                    [sg.VStretch()],
                    [add_dots(), sg.Canvas(size=(half_measure,two), pad=two), sg.Stretch(), add_dots(), sg.Stretch(), sg.Canvas(size=(half_measure,two), pad=two), add_dots()],
                    [sg.VStretch()],
                    [sg.Stretch(), sg.Text(point_value, key="point_output", font=(f"courier {int(std_dot_size) + 4} bold"), pad=0), sg.Stretch()],
                    [sg.VStretch()],
                    [add_dots(), sg.Canvas(size=(half_measure,two), pad=two), sg.Stretch(), add_dots(), sg.Stretch(), sg.Canvas(size=(half_measure,two), pad=two), add_dots()],
                    [sg.VStretch()],
                    ]

    column_3 =      [[sg.VStretch()],
                    [sg.Canvas(size=(200,two)), add_dots(), sg.HSeparator(color="gold"), add_dots(), sg.Canvas(size=(200,two))],
                       [sg.Canvas(size=(widest_measure,two))],
                    #[add_dots(), sg.Stretch(), sg.HSeparator(color="gold"), sg.Stretch(), add_dots()],
                    [sg.Stretch(), sg.Text(output_line_str, key="output_line", font=(f"courier {int(std_dot_size) + 4} bold"), pad=0), sg.Stretch()],
                    [sg.VStretch()]
                    ]

    tally = [
            [sg.Stretch(), sg.T(SYMBOL_DOWN, enable_events=True, k='-OPEN SEC1-', text_color='yellow'), sg.T('Tally Board', enable_events=True, text_color='yellow', k='-OPEN SEC1-TEXT'), sg.Stretch()],
            [collapse(tally_board, '-SEC1-')]
            ]

    main_contents_vert = [
            [sg.Column(layout=column_one_vert, justification="center")], [sg.Column(layout=column_two_vert, justification="center")], [sg.Column(layout=column_3, justification="center", expand_x=True)], [sg.Column(layout=tally, justification="center")]
        ]

    layout = [[sg.Frame(title=" farkle ••", layout=main_contents_vert, font=("courier", std_dot_size, "bold"), relief="groove", pad=(5), border_width=5)]]

    window = sg.Window('FARKLE', layout, keep_on_top=True, finalize=True, alpha_channel=1.0, grab_anywhere=True, no_titlebar=True, use_custom_titlebar=True, titlebar_background_color="#332b26", titlebar_text_color="#ffd768", titlebar_font="courier 10 bold", icon=icon_str)
    window['-TAKE-'].bind("<Return>", "_Enter")


    colour_buttons(preroll=True)
    game_started = False
    round_started = False
    opened1 = False
    window['-SEC1-'].update(visible=False)

    while True:
        #print(f"Dice.by_no at start of window: \n{dice.by_no}")
        #exit()
        colour_buttons(preroll=True if not round_started else False, do_refresh=False if round_started else True)

        event, values = window.read(timeout=1000)

        used_dice = None
        if players.is_singleplayer and players.current == players.player_2:
            round_started = True
            outcome, used_dice = gui_autoplay(players.current, used_dice) # game_won end_turn bust
            if outcome:
                print(f"OUTCOME: {outcome}")
                if outcome == "end_turn":
                    round_started = take_score_and_end_turn(get_turnscore=False)

                elif outcome == "bust":
                    #colour_buttons(do_refresh=True, bust=True)
                    players.current.turn_score = 0
                    write_points(bust=True)
                    reset_for_new_turn()
                    round_started = False
                elif outcome == "game_won":
                    game_won(players.current)
                    exit()

        """if not round_started:
            for i, die_inst in dice_dict.items():
                roll_single(i, die_inst)
                window[i].update()
                sleep(.05)
"""
        if not round_started:

            clear_held_and_used()
            write_points(string_print=f"{players.current.name} is starting their turn.")
            sleep(.2)
            update_output_line(text='')

            roll_dice(do_refresh=True)
            score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice), print_result=False, get_score=False)
            round_started = True
            update_output_line(text=output_str)
            if not used_dice:
                write_points(bust=True)
                colour_buttons(do_refresh=True, bust=True)
                sleep(.8)
                reset_for_new_turn()
                round_started = False

        if event.startswith('-OPEN SEC1-'):
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
            update_output_line(text=output_str)
            print(f"SCORE: {score}")
            write_points(players.current.turn_score + score)

        if event == "-ROLL-" and round_started:
            clear_prints()
            held_dice = set(i for i in dice.dice if i.held)
            if not held_dice:
                update_output_line("You must hold at least one die before rolling.")
            else:
                preroll_score, _, _ = get_score(players.current, held_dice, print_result=False, get_score=False)
                mark_used(held_dice)
                used_dice = set(i for i in dice.dice if i.used)
                if used_dice and len(used_dice) == 6:
                    update_output_line(f"{players.current.name} used all their dice; rerolling all.")
                    clear_held_and_used()
                    #colour_buttons()

                roll_dice(do_refresh=True)
                score, used_dice, output_str = get_score(players.current, set(i for i in dice.dice if not i.used), print_result=False, get_score=False)
                update_output_line(text=output_str)
                if not used_dice:
                    write_points(bust=True)
                    colour_buttons(do_refresh=True, bust=True)
                    sleep(.8)
                    reset_for_new_turn()
                    round_started = False
                else:
                    players.current.turn_score += preroll_score

        if event == "-TAKE-":
            round_started = take_score_and_end_turn()

        if event == sg.WIN_CLOSED or event == '-EXIT-':
            clear_prints()
            break

        if event == "-SETTINGS-":
            clear_prints()
            window.close()
            return None, "use_settings"

    window.close()
    return "exit", None


def settings_window():

    #return #UNDO ME

    def make_settings_button(width:float=std_btn, height:float=std_btn, key:str="", key_str:str="Pause", tooltip_str=''):
        if key:
            key_formatting = key
        else:
            key_upper = key_str.upper()
            key_formatting = str("-" + key_upper + '-')
        #sg.Button("Hello", , use_ttk_buttons=True)
        return sg.Button(auto_size_button=True, button_text = key_str, key=key_formatting, mouseover_colors=button_mouseover, use_ttk_buttons=True, size=(width,height), font=(f"courier {std_dot_size} bold"), disabled_button_color = "#756C5F", tooltip=tooltip_str)

    def make_playstyle_buttons():
        playstyle_buttons = []
        playstyle_buttons.append(sg.Stretch())
        for style in players.playstyles:
            playstyle_buttons.append(sg.Stretch())
            playstyle_buttons.append(make_settings_button(width=std_btn, height=1, key=style, key_str=f"[ {style} ]"))
        playstyle_buttons.append(sg.Stretch())
        playstyle_buttons.append(sg.Stretch())
        return playstyle_buttons

    singleplayer_open = mode_open = names_open = themes_open = False

    singleplayer = [
                     [sg.HSeparator(color="gold")],
                     [sg.Text("Currently, the game is single player. What do you want it to be?" if players.is_singleplayer else "Currently, the game is two-player. What do you want it to be?")],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [make_settings_button(width=std_btn, height=1, key="choose_single", key_str="Single player"), sg.Stretch(), make_settings_button(width=std_btn, height=1, key="choose_two", key_str="Two human players")],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [sg.HSeparator(color="gold")]
                    ]

    mode = [
                     [sg.HSeparator(color="gold")],
                     [sg.Text(f"Currently, the computer is using the playstyle `{players.default_playstyle}` game is single player. What do you want it to be?", justification="center")],
                     #[sg.Text(f"The options are: {list(f"[ {i} ]" for i in players.playstyles)}`", justification="center")],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     make_playstyle_buttons(),
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [sg.HSeparator(color="gold")]
                    ]

    names = [
                     [sg.HSeparator(color="gold")],
                     [sg.Text(f"Player 1 is currently named `{players.player_1.name}`. Player 2 is current named `{players.player_2.name}`", justification="center")],
                     [sg.Text(f"Enter new names below to change them. (Entering nothing will keep the existing name(s).)", justification="center")],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [sg.Input(default_text=players.player_1.name, key="player_1_name", focus=True, enable_events=True), sg.Input(default_text=players.player_2.name, key="player_2_name", enable_events=True)],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [sg.HSeparator(color="gold")]
                    ]

    themes = [
                     [sg.HSeparator(color="gold")],
                     [sg.Text(f"Currently, the computer is using the playstyle `{players.default_playstyle}` game is single player. What do you want it to be?", justification="center")],
                     [sg.Text(f"The options are: {str(f"[ {i} ]" for i in players.playstyles)}`", justification="center")],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [make_settings_button(width=std_btn, height=1, key="choose_single", key_str="Single player"), sg.Stretch(), make_settings_button(width=std_btn, height=1, key="choose_two", key_str="Two human players")],
                     [sg.Canvas(size=(widest_measure,two), pad=two)],
                     [sg.HSeparator(color="gold")]
                    ]


    settings_options = [[make_settings_button(width=std_btn, height=1, key="panel_single_player", key_str="Single player"), add_dots(), sg.HSeparator(color="gold"), add_dots(),
                         make_settings_button(width=std_btn, height=1, key="panel_mode", key_str="Computer Mode"), add_dots(), sg.HSeparator(color="gold"), add_dots(),
                         make_settings_button(width=std_btn, height=1, key="panel_names", key_str="Player names"), add_dots(), sg.HSeparator(color="gold"), add_dots(),
                         make_settings_button(width=std_btn, height=1, key="panel_themes", key_str="Colour themes")],
                        [sg.Stretch(), collapse(singleplayer, '-SEC1-'), collapse(mode, '-MODE-'), collapse(names, '-NAMES-'), collapse(themes, '-THEMES-'), sg.Stretch()],
                        [sg.Stretch(), make_settings_button(width=std_btn, height=1, key="leave", key_str="Save changed settings", tooltip_str="Restart game with the new settings."), sg.Stretch(), make_settings_button(width=std_btn, height=1, key="leave_no_save", key_str="Return without saving", tooltip_str="Closing the settings window without saving changes."), sg.Stretch()]
                        ]

    settings_main = [[sg.Column(settings_options)]]

    settings_layout = [[sg.Frame(title=" farkle settings ••", key="settings_window", layout=settings_main, font=("courier", std_dot_size, "bold"), relief="groove", pad=(5), border_width=5)]]

    settings_window = sg.Window('SETTINGS', settings_layout, keep_on_top=True, finalize=True, alpha_channel=1.0, grab_anywhere=True, no_titlebar=True, use_custom_titlebar=True, titlebar_background_color="#332b26", titlebar_text_color="#ffd768", titlebar_font="courier 10 bold", icon=icon_str)

    settings_dict = {}

    while True:

        event, values = settings_window.read(timeout=1000)

        if event.startswith("panel_"):
            if event == "panel_single_player": # should be a dropdown menu
                if mode_open:
                    settings_window['-MODE-'].update(visible=False)
                if names_open:
                    settings_window['-NAMES-'].update(visible=False)
                if themes_open:
                    settings_window['-THEMES-'].update(visible=False)

                singleplayer_open = not singleplayer_open
                settings_window["choose_single"].update(disabled=True if players.is_singleplayer else False)
                settings_window["choose_two"].update(disabled=False if players.is_singleplayer else True)
                settings_window['-SEC1-'].update(visible=singleplayer_open)

            if event == "panel_mode":
                if singleplayer_open:
                    settings_window['-SEC1-'].update(visible=False)
                if names_open:
                    settings_window['-NAMES-'].update(visible=False)
                if themes_open:
                    settings_window['-THEMES-'].update(visible=False)

                mode_open = not mode_open
                for style in players.playstyles:
                    settings_window[style].update(disabled=True if players.default_playstyle == style else False)

                settings_window['-MODE-'].update(visible=mode_open)

            if event == "panel_names":
                if singleplayer_open:
                    settings_window['-SEC1-'].update(visible=False)
                if mode_open:
                    settings_window['-MODE-'].update(visible=False)
                if themes_open:
                    settings_window['-THEMES-'].update(visible=False)

            if event == "panel_themes":
                if singleplayer_open:
                    settings_window['-SEC1-'].update(visible=False)
                if mode_open:
                    settings_window['-MODE-'].update(visible=False)
                if names_open:
                    settings_window['-NAMES-'].update(visible=False)

                themes_open = not themes_open
                settings_window['-THEMES-'].update(visible=themes_open)

        if values and values.get("player_1_name"):
            settings_dict["change_names"] = values

        if event == "choose_single":
            settings_dict["set_singleplayer"] = True
            settings_window["choose_single"].update(disabled=True)
            settings_window["choose_two"].update(disabled=False)

        if event == "choose_two":
            settings_dict["set_singleplayer"] = False
            settings_window["choose_single"].update(disabled=False)
            settings_window["choose_two"].update(disabled=True)

        if event == "mode":
            print(f"Currently the PC's playstyle is `{players.default_playstyle}`")
            print("Change the PC player's playstyle here.")

        if event == "names":
            #    init_classes(player1, player2, player1_col = "blue", player2_col = "red")
            print("Set the names here.")

        if event == "leave":
            #print("Save settings to the json file and exit the settings menu.")

            settings_window.close()
            return settings_dict

        if event == "leave_no_save":
            settings_window.close()
            return


def apply_settings(settings_dict):
    for action, data in settings_dict.items():
        if action == "set_singleplayer":
            print(f"action is set_singleplayer: true/false: `{data}`")
            players.is_singleplayer = data
            init_classes(players.player_1.name, '', player1_col = "blue", player2_col = "red")
        if action == "change_names":
            print(f"DATA for change names: {data}")
            for name in data:
                if data[name]:
                    print(f"NAME: {name}")
                    if name == "player_1_name":
                        players.player_1.name = data[name]
                    else:
                        players.player_2.name = data[name]




def main_gui():

    make_play_area() # needed for pos initialisation.
    global players
    players = playerClass()
    pick_player_names("Player_1", "Player_2")

    while True:

        close_window, use_settings = make_window()
        if close_window:
            break
        elif use_settings:
            settings_dict = settings_window()
            if settings_dict:
                apply_settings(settings_dict)

#main()
main_gui()

"""
NOTE:
Currently if you select all dice and reroll, it just lets you reroll everything. No limit as to having to have at least one valid selection. Need to fix that."""
