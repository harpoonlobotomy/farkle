"""simple text-based farkle game
started April 2026 //  v.08 // harpoonlobotomy"""

from time import sleep
#positions = ["   [  1  ]   ", "   [  2  ]   ", "   [  3  ]   ", "   [  4  ]   ", "   [  5  ]   ", "   [  6  ]   "]
positions = "[  1  ]      [  2  ]      [  3  ]      [  4  ]      [  5  ]      [  6  ]"
END = "\033[0m"
HIDE = "\033[?25l"
SHOW = "\033[?25h"
colours = {
    "red": "\033[1;31m",
    "green": "\033[1;32m",
    "yellow": "\033[1;33m",
    "blue": "\033[1;34m",
    "magenta": "\033[1;35m",
    "cyan": "\033[1;36m",
}

export_data = True

class outputter:

    def __init__(self):
        from uuid import uuid4
        self.session_ID:str = str(uuid4())[-6:]
        self.turn_data = {}
        self.game_data = {}

    def start_game(self):

        self.game_data = {self.session_ID: {0: {}}}


    def output_gamedata(self, player, turn = None, end_game=False):

        force_no_writing = True
        if force_no_writing:
            return

        """
        data = self.turn_data

        if not self.game_data or not self.game_data.get(self.session_ID):
            self.start_game()

        print(f"self.game_data[self.session_ID]: {self.game_data[self.session_ID]}\n\n")
        if not self.game_data[self.session_ID].get(players.total_games):
            self.game_data[self.session_ID][players.total_games] = self.turn_data

        elif not turn:
            for turn in self.turn_data:
                self.game_data[self.session_ID][players.total_games].update(self.turn_data)

        else:
            if self.game_data[self.session_ID][players.total_games].get(turn):
                self.game_data[self.session_ID][players.total_games][turn].update(self.turn_data.get(turn))
            else:
                self.game_data[self.session_ID][players.total_games][turn] = self.turn_data.get(turn)
        """
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


        """
        if not farkle_file.get(self.session_ID):
            farkle_file[self.session_ID] = dict({players.total_games: data})

        if farkle_file[self.session_ID].get(players.total_games):
            for turn in data:
                if farkle_file[self.session_ID][players.total_games].get(turn):
                    farkle_file[self.session_ID][players.total_games][turn].update(data[turn])
                else:
                    farkle_file[self.session_ID][players.total_games][turn] = data[turn]

        else:
            farkle_file[self.session_ID][players.total_games] = data

"""
        with open(file, "w") as f:
            json.dump(gamedata, f, indent=2)


    def collect_turndata(self, player, matches=None, dice=None, bust=False, turn_end=None, game_end=False):

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

        if dice:
            if not isinstance(dice, list|set|tuple):
                dice = list(dice)

        if self.turn_data and self.turn_data.get(players.total_turns):
            current_data = self.turn_data[players.total_turns]
        else:
            self.turn_data[players.total_turns] = {"player": player.name, "rolls": []}
            current_data = self.turn_data[players.total_turns]

        if matches:
            current_data["rolls"].append({"Dice": list(i.value for i in dice), "matches": matches})

        if bust:
            current_data["rolls"].append({"Dice": list(i.value for i in dice), "matches": "BUST"})
            current_data["turn_end_score"] = {0: player.game_score}

        if turn_end:
            current_data["turn_end_score"] = {player.turn_score: player.game_score}
            if write_turn_data:
                self.output_gamedata(player)

        self.game_data.setdefault(self.session_ID, {}).setdefault(players.total_games, {}).setdefault(players.total_turns, current_data)

        if game_end:
            self.output_gamedata(player, end_game=True)


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
                #self.print_error(f"Printing 'part' of text: {part}")
                centred_text = int((self.columns - len(part))/2)-1
                centred_text = (" " * centred_text) + part + (" " * centred_text)
                #self.print_error(f"centred: {centred_text}", 2)
                text = self.points_line + ("\n" * i) + centred_text + self.clearline + END # will break visually if too many newlines in a string, but works well for single line breaks.
                print(text, end = '')
                if delay:
                    sleep(.02)

        else:
            centred_text = int((self.columns - len(text))/2)-1
            centred_text = (" " * centred_text) + text + (" " * centred_text)
            text = self.points_line + centred_text + self.clearline + END
            print(text, end = '')


    def print_dice(self, text='', die=None, skin=''):

        skin = colours[skin] if colours.get(skin) else skin
        #print(HIDE, end='') # 34
        if die:#"                                [  1  ]      [  2  ]      [  3  ]      [  4  ]      [  5  ]      [  6  ]"
            temp = self.dice_line.replace("7f", f"{self.dice_pos.get(die.place_no)}f")

        if isinstance(text, list):
            text = ''.join(text)

        if die:
            text = temp + skin + text + END
        else:
            text = self.dice_line + text
        print(text, end = '')

    def print_prompt(self, text):

        centred_text = int((self.columns - len(text))/2)-1
        centred_text = (" " * centred_text) + text + (" " * centred_text)
        text = self.prompt_line + centred_text + self.clearline + END
        print(text, end = '')


    def print_input(self, text):

        #print(f"{self.input_line}", end='')
        #print("\033[0J")
        centred_text = int((self.columns - len(text))/2)-1
        centred_text = (" " * (centred_text - 12)) + text
        text = self.input_line + "\033[2;36m" + centred_text + self.clearline + END
        print(text, end = '')


    def print_output(self, text, clear=False):

        if clear:
            text = print(self.output_line, self.clearline, end='')
            return
        print(f"{self.output_line}{self.clearline}")#self.output_line + text + self.clearline + END)
        centred_text = int((self.columns - len(f"[  {text}  ]"))/2)-1
        centred_text = (" " * centred_text) + "[  " + text + "  ]"
        text = self.output_line + "\033[2;36m" + centred_text + END
        print(text, end='')
        #print(self.clearline, end='')

def get_input():
    pos.print_input(">> ")
    #print(SHOW, end='')
    test = input()
    #print(HIDE, end='')
    pos.print_input("     ") # to clear the line once input is accepted.
    return test

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

    #print(f"POS:\n{pos}")
    #print(f"{pos.error_line} ERROR_LINE")
    #print(f"{pos.points_line} POINTS LINE")
    #print(f"{pos.dice_line} DICE LINE")
    #print(f"{pos.prompt_line} PROMPT LINE")
    #print(f"{pos.input_line} INPUT LINE")
    #print(f"{pos.output_line} OUTPUT LINE")
    """
    ESC[{line};{column}H
ESC[{line};{column}f	moves cursor to line #, column

ESC[s	save cursor position (SCO)
ESC[u

        self.dice_line:str = ""
        self.prompt_line:str = ""
        self.input_line:str = ""
        self.output_line:str = ""
    """

class die:
    def __init__(self, place_number = 1, skin=None):
        self.value = 1
        self.place_no = place_number
        self.held = False
        self.used = False #for dice that have been rolled and kept aside, to stop them being recounted and acted on thereafter.
        self.skin = skin

    def __repr__(self):
        return f"<place_no: {self.place_no} / value: {self.value} / used: {self.used} / held: {self.held}>"

class dice_data:

    def __init__(self):

        self.skin = None
        self.dice:set[die] = set()
        self.by_no:dict[int, die] = {} # by_no is int, not str
        self.held_dice:set[die] = set()


    def init_dice(self):

        for i in range(1, 7):
            self.dice.add(die(place_number=i, skin=self.skin))
        self.by_no = {die.place_no: die for die in self.dice}


    def print_updated(self, die = None, skin = None):

        def print_die(die, skin):
            if isinstance(die, int):
                die = self.by_no[i]
            if skin:
                die_skin = skin# red for unheld dice
            else:
                die_skin = die.skin if die.skin else colours.get("red") # should allow for per-die skin, as well as default skin (which can be set by dice set on init or by player)
                if die.held:
                    die_skin = colours.get("green") # green for held dice
                    die_skin = "\033[2m" + die_skin # dim the held dice a bit to make them more visually distinct from unheld dice
                elif die.used:
                    die_skin = colours.get("yellow")

            pos.print_dice(text = f"[  {die.value}  ]", die=die, skin=die_skin)
            sleep(.01)

        if not die:
            for i in range(1, 7):
                print_die(i, skin)

        else:
            print_die(die, skin)


    def set_default_val(self):

        val = 1
        for die in dice.dice:
            if dice.skin and (not die.skin or die.skin == "default" or die.skin != dice.skin):
                die.skin = dice.skin

            die.place_no = die.value = val # place 1-6 in that order
            val += 1
            dice.print_updated(die, skin="magenta")
            sleep(.03)

    def apply_playstyle(self, player:"playerInst", turn_score, available_dice:set[die]):

        playstyle_rules = {

            "harpoon": {
                "take_risk": [
                    (players.opponent.game_score - 2000) > player.game_score,
                    players.opponent.game_score > 3200,
                    turn_score < 500
                    ],
                "requirements": {
                    "in_dice": [1, 5],
                    "all_dice_used": True
                    }
            }
        }
        print(f"TURN SCORE: {turn_score}")
        input()
        use_dice = set()
        if player.playstyle and player.playstyle in playstyle_rules:
            for risk_reason in playstyle_rules[player.playstyle]["take_risk"]:
                if not risk_reason:
                    continue
                for item in playstyle_rules[player.playstyle]["requirements"]:
                    if use_dice:
                        break
                    if item == "in_dice":
                        if 1 in playstyle_rules[player.playstyle]["requirements"][item]:
                            onedice = list(i for i in available_dice if i.value == 1)
                            if onedice:
                                use_dice.add(onedice[0])
                            elif 5 in playstyle_rules[player.playstyle]["requirements"][item]:
                                    onedice = list(i for i in available_dice if i.value == 5)
                                    if onedice:
                                        use_dice.add(onedice[0])

        if use_dice:
            print(f"USE DICE: {use_dice}")
            return turn_score, use_dice

        return turn_score, None


    """def auto_best(self, player=None, output_results=True, is_auto=True):
        #pos.print_error("AUTO_BEST")
        matches = {}
        used_dice = set()

        if is_auto:
            die_set = set(i for i in dice.dice if not i.used)
        else:
            die_set = set(i for i in dice.dice if not i.used and i.held)

        vals = list(i.value for i in die_set)
        #pos.print_points(f"VALS at top: {vals}")
        if len(set(vals)) == 6:
            used_dice = die_set
            matches["full house"] = ({1: {1: 1500}})
            #print(f"MATCHES after full house: {matches}")

        elif len(set(vals)) >= 5:
            #pos.print_error(f"VALS: {vals}", 1)
            small_straight = set(i for i in (1, 2, 3, 4, 5) if i in set(vals))
            if not small_straight or (small_straight and len(small_straight) < 5):
                small_straight = set(i for i in (2, 3, 4, 5, 6) if i in set(vals))
            if small_straight and len(small_straight) == 5:
                used_dice.update(set(i for i in die_set if len(used_dice) < 5 and i.value in small_straight and i not in used_dice))
                pos.print_error(f"Used dice after small straight: {used_dice}", 3)
            #if all(i for i in ("1", "2", "3", "4", "5") if i in vals) or all(i for i in vals in ("2", "3", "4", "5", "6")):
                matches["small straight"] = ({"small_straight": {1: 750}})


        for item in vals:
            count = sum(1 for die in die_set if die.value == item)
            if count >= 3:
                if item == 1:
                    used_dice.update(set(i for i in die_set if i not in used_dice and i.value == item))
                    matches["three (or four) of a kind"] = ({item: {count: int(1000 * (count - 2))}})
                else:
                    used_dice.update(set(i for i in die_set if i not in used_dice and i.value == item))
                    matches["three (or four) of a kind"] = ({item: {count: int(item * 100 * (2 ** (count - 3)))}})

        remaining_dice_selection = set(i for i in die_set if i not in used_dice)
        if remaining_dice_selection:
            pos.print_error(f"Remaining dice: {remaining_dice_selection}", 2)
            vals = set(i.value for i in remaining_dice_selection)
            for item in vals:
                count = sum(1 for die in remaining_dice_selection if die.value == item and die not in used_dice and not die.used)
                if count:
                    if item == 1:
                        #pos.print_error(f"item == 1", 1)
                        used_dice.update(set(i for i in remaining_dice_selection if i.value == item and i not in used_dice and not i.used))
                        matches["single ones"] = ({item: {count: int(100 * count)}})
                    elif item == 5:
                        #pos.print_error(f"item == 5", 2)
                        used_dice.update(set(i for i in remaining_dice_selection if i.value == item and i not in used_dice and not i.used))
                        matches["single fives"] = ({item: {count: int(50 * count)}})
        #pos.print_error(f"MATCHES: {matches}", 2)
        #else:
            #pos.print_error(f"USED DICE: {used_dice}", 3)

        if matches:
            if output_results:
                to_json.collect_turndata(players.current, matches, dice=used_dice)

            best_option = None
            best_value = 0
            for category in matches:
                for item, value in matches[category].items():
                    count, value = list(value.items())[0]
                    if value > best_value:
                        best_value = value
                        best_option = category
                        if "house" in best_option or "straight" in best_option:
                            extra = ''
                        else:
                            extra = f" with {count} {item}'s"
                        best_option = best_option + extra
                    elif value == best_value:
                        best_option = best_option + " / " + category
            #pos.print_error(f"Best option: `{best_option}`{extra} for {best_value} points.", 3)

        if not matches:
            to_json.collect_turndata(players.current, dice=die_set, bust=True)
            pos.print_output(f"BUST! Ending {players.current.name}'s turn.")
            if (players.autoplay and isinstance(players.autoplay, playerInst) and players.current != players.autoplay) or not players.autoplay:
                pos.print_prompt("Press enter to continue.")
                input()
            else:
                sleep(.8)
            return False, None

        else:
            if player: # only for NPC
                dice.apply_playstyle(player)

            return matches, used_dice#best_value"""


    """def dice_potential(self, starting=False): # NOT USED ANYMORE. Remove once certain.
        #pos.print_error(f"DICE POTENTIAL")
        matches = {}
        if starting:
            dice_selection = "dice"
            #vals = set(i.value for i in dice.dice)
        else:
            dice_selection = "held_dice"
        vals = set(i.value for i in getattr(dice, dice_selection) if not i.used)
        for item in vals:
            count = sum(1 for die in getattr(dice, dice_selection) if die.value == item and not die.used)
            if count >= 3:
                if item == 1:
                    matches["three (or four) of a kind"] = ({item: {count: int(1000 * (2 ** (count - 3)))}})
                else:
                    matches["three (or four) of a kind"] = ({item: {count: int(item * 100 * (2 ** (count - 3)))}})
            else:
                if item == 1:
                    matches["single ones"] = ({item: {count: int(100 * count)}})
                elif item == 5:
                    matches["single fives"] = ({item: {count: int(50 * count)}})

        if len(vals) == 6:
            matches["full house"] = ({item: {count: 1500}})
        elif len(vals) == 5:
            #pos.print_error(f"VALS: {vals}", 1)
            small_straight = list(i for i in (1, 2, 3, 4, 5) if i in vals)
            if not small_straight or (small_straight and len(small_straight) < 5):
                small_straight = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            if small_straight and len(small_straight) == 5:
            #if all(i for i in ("1", "2", "3", "4", "5") if i in vals) or all(i for i in vals in ("2", "3", "4", "5", "6")):
                matches["small straight"] = ({item: {count: 750}})

        #pos.print_error(f"MATCHES: {matches}", 2)
        if matches:
            best_option = None
            best_value = 0
            for category in matches:
                for item, value in matches[category].items():
                    count, value = list(value.items())[0]
                    if value > best_value:
                        best_value = value
                        best_option = category
                        #print(f"CATEGORY: {best_option}")
                        if "house" in best_option or "straight" in best_option:
                            extra = ''
                        else:
                            extra = f" with {count} {item}'s"
                    elif value == best_value:
                        best_option = best_option + " / " + category
            #pos.print_error(f"Best option: `{best_option}`{extra} for {best_value} points.", 3)

        if not matches:
            if starting:
                pos.print_output("BUST! Ending turn.")
                sleep(.8)
                return False
            else:
                print(f"{pos.output_line}No matches but not starting. Should this bust too?")
        else:
            return matches#best_value

        return True"""

    def roll(self):

        forced_rolls = {
            #1: [1, 1, 1, 1, 1, 1],
            1: [1, 1, 1, 1, 1, 5],
            2: [1, 2, 3, 4, 5, 6],
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


    def hold(self, place_no, player): # selecting by place_no; if there was a graphic, they would scatter to roll then scoot back to their positions.

        if place_no not in self.by_no:
            print(f"self.by_no: {self.by_no}")
            raise ValueError(f"[die with place_no `{place_no}` does not exist]")

        die = self.by_no.get(place_no)

        if die.held:
            die.held = False
            dice.held_dice.remove(die)
            #player.held_score -= die.value
            #self.hold_formatting(die)
        else:
            die.held = True
            #player.held_score += die.value
            dice.held_dice.add(die)
            #self.hold_formatting(die)
        self.print_updated()

dice = dice_data()

class playerInst:

    def __init__(self, player_name, skin = None):

        self.name = player_name
        self.turn_score = 0
        self.skin = skin
        self.turn_count = 0
        self.game_score = 0
        self.wins = 0
        self.losses = 0
        self.held_dice = None

        self.playstyle = ''

    def __repr__(self):
        return f"[(player: {self.name} // held_score: {self.held_dice} // turn_score: {self.turn_score})]"

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
        self.players:set = set()
        self.current:playerInst = None
        self.opponent:playerInst = None
        self.autoplay = False
        self.playstyles:list = ["simple", "harpoon"]

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
        pos.print_output(f"Switching players, next up is {players.current.name}...")
        print()
        sleep(1.8)


def init_classes(player1 = "player_1", player2 = "player_2", player1_col = "red", player2_col = "blue", single_player=True):

    player_1 = playerInst(player1, skin=player1_col)
    players.players.add(player_1)
    players.current = player_1

    player_2 = playerInst(player2, skin=player2_col)
    players.players.add(player_2)
    players.opponent = player_2

    if single_player == True:
        players.autoplay = player_2
        if not player_2.playstyle:
            import random
            player_2.playstyle = random.choice(players.playstyles)

    dice.init_dice()
    dice.set_default_val()

    return dict({"player_1": player_1, "player_2": player_2})

def get_dice_by_val(i, val, player, in_loop:set[die]):
    #print(f"val in test.split: {val}")
    for i in range(1, 7):
        inst  = dice.by_no.get(i)
        #print(f"item: {i} // inst: {inst}")
        if inst.value == int(val) and inst not in in_loop and not inst.used:
            val = i
            #print(f"(Holding die in position [{val}])")
            dice.hold(val, player)#players.get(player) if player_1 else players.get("player_2"))
            in_loop.add(inst)
            return in_loop
        #elif inst.value == int(val) and inst in in_loop:
            #print(f"(Already held die with value {val} in this turn, skipping.)")
    return in_loop

def get_score(player=None, autoplay_dice=None, print_result=True, get_score=True):

    if autoplay_dice:
        dice_selection = set(autoplay_dice)
    else:
        dice_selection = dice.held_dice # Not used anymore, will remove later.

    held_score = 0
    vals = set(i.value for i in dice_selection)

    score_dict = {i:None for i in dice_selection}

    used_dice = set()
    if len(vals) == 6:
        used_dice = dice_selection
        score_dict = {i:"full house" for i in dice_selection}
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
            else:
                #print(f"Match count: {match_count}")
                held_score += 1000 * (match_count-1)

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
                elif item == 5:
                    #pos.print_error(f"item == 5", 2)
                    used_dice.update(set(i for i in remaining_dice_selection if i.value == item and i not in used_dice and not i.used))
                    #matches["single fives"] = ({item: {count: int(50 * count)}})
                    held_score += 50 * count

    no_playstyle = True
    if not no_playstyle:
        if player and player.playstyle and (used_dice and len(used_dice) != len(dice_selection)): # only for NPC
            held_score, updated_dice = dice.apply_playstyle(player, held_score, dice_selection)
            if updated_dice:
                used_dice = updated_dice

    if print_result:
        pos.print_output(f"{player.name} can score {held_score} points here if they choose to take the points, taking their total score to {player.game_score + player.turn_score + held_score}.")
    if get_score:
        player.turn_score += held_score
    return held_score, used_dice

def clear_held_and_used():

    for die in dice.dice:
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
    #pos.print_error(f"updating tally for {players.current.name}")

    players.tally[players.total_turns] = (players.current.name, players.current.game_score)
    count = int(pos.tally)
    column = 4
    #print(HIDE, end='')
    for i, entry in players.tally.items():
        #print(f"ENTRY: {entry} / type: {type(entry)}")
        name, score = entry
        #print(f"NAME: {name} SCORE: {score}")
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

    pos.print_output(f"Player {player.name} ends their turn with a score of {player.game_score}.")
    sleep(.8)
    print()
    clear_held_and_used()

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

    used = list(i for i in dice.dice if i.used)
    if used and len(used) == 6: #NOTE: Not working properly yet.
        pos.print_output("All dice used, resetting for next roll.")
        for die in used:
            die.used = False

    dice.roll()

def take_roll(player:playerInst):

    player.game_score += player.turn_score
    if export_data:
        to_json.collect_turndata(player, turn_end=True)
    if end_turn(player):
        return "game over"

def autoplay(player:playerInst):
    """for player_2 to be PC controlled. super basic."""

    while True:
        unused_dice = set(i for i in dice.dice if not i.used)
        dice.print_updated()
        pos.print_output("Getting score...")
        has_potential, used_dice = get_score(player, unused_dice, print_result=False, get_score=False)
        #has_potential, used_dice = dice.auto_best(player)
        #pos.print_error(f"HAS POTENTIAL: {has_potential}")# USED DICE: {used_dice}")
        #has_potential = dice.dice_potential(starting=True)
        if not has_potential:
            #player.game_score = 0#+= player.turn_score
            pos.print_output(f"BUST! Ending {players.current.name}'s turn.")
            sleep(.3)
            player.turn_score = 0
            clear_held_and_used()
            return end_turn(player)

        for i in used_dice:
            i.held = True

        dice.print_updated()
        sleep(.4)
        score, used_dice = get_score(player, used_dice)

        mark_used(used_dice)
        sleep(.4)

        used_dice_count = sum(1 for d in dice.dice if d.used)

        if (used_dice_count) == 6:
            pos.print_prompt("All dice used. Do you want to [reroll] or [take] the current score? (Enter 'reroll' or 'take')")
            if player.game_score + player.turn_score >= 4000:
                return take_roll(player)

            clear_held_and_used()
            do_roll()

        else:
            dice.print_updated()

            sleep(.8)
            if used_dice_count < 4:
                do_roll()
                pos.print_output("Roll done, checking for potential...")
            else:
                sleep(.5)
                return take_roll(player)


def play_turn(player:playerInst):

    opponent = players.opponent
    #print(f"{pos.error_line}OPPONENT: {opponent} / name: {opponent}")

    if player.skin:
        dice.skin = player.skin
    else:
        dice.skin = ""
    player.turn_count += 1
    pos.print_points(f"Current turn: {player.turn_count}  Current player: {player.name}. \n{player.name} has {player.game_score} points. {players.opponent.name} has {opponent.game_score} points.")
    pos.print_output(f"{player.name} is rolling...")
    dice.set_default_val()
    dice.print_updated()
    dice.roll()

    """
    turn_score = int used holding the score of a single turn,  without considering past turns in this game.
    game_score = int used for holding player score for the current game, adding each turn_score when the held dice are added.
    """
    in_loop = set()
    reserved = 0
    while True:
        if players.autoplay and ((isinstance(players.autoplay, playerInst) and player == players.autoplay) or isinstance(players.autoplay, bool)):
            return autoplay(player)

        #has_potential, _ = dice.auto_best(output_results=False)
        die_set = in_loop if in_loop else set(i for i in dice.dice if not i.used)
        #input(f"\n\n\ndie set: {die_set}")
        has_potential, _ = get_score(player, autoplay_dice=die_set, print_result=True if in_loop else False, get_score=False)
        #pos.print_error(f"HAS POTENTIAL: {has_potential}")
        if not has_potential:
            player.turn_score = 0
            to_json.collect_turndata(players.current, dice=die_set, bust=True)
            pos.print_output(f"BUST! Ending {players.current.name}'s turn.")
            sleep(.3)
            clear_held_and_used()
            return

        if in_loop:
            pos.print_prompt("Enter more values to add to the selection, or hit enter to take the selected dice.")
        else:
            pos.print_prompt("Enter the values of the dice you want to hold.")

        test = get_input()
        #pos.print_input(f"        >> {SHOW}")

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
            score, _ = get_score(player, in_loop)

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
                    if (test.lower() in ("take", "t")) or not test:
                        return take_roll(player)

                    elif test.lower() in ("roll", "r"):
                        do_roll()
                        break
                    else:
                        pos.print_error("Invalid input, please enter `take` or `roll`.")

def print_wins():
    sleep(.3)
    pos.print_points(f"{players.current.name} has won {players.current.wins} game(s).  {players.opponent.name} has one {players.opponent.wins} game(s).")
    print()
    sleep(.8)


def pick_player_names(single_player=False):

    pick_names = True
    player1 = "player_1"
    player2 = "player_2"

    check_names = False

    if pick_names:
        while True:
            pos.print_prompt("Enter the name for Player 1: ")
            player1 = get_input()

            if not player1:
                pos.print_output(f"Defaulting to `player_1`. Press 'enter'")
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

        init_classes(player1, player2, player1_col = "red", player2_col = "blue", single_player=single_player)

        while True:
            if single_player:
                not_choose_playstyle = True
                if not_choose_playstyle:
                    players.autoplay.playstyle = "simple"
                    break

                else:
                    names = [f"[ {i} ]  " for i in players.playstyles]
                    pos.print_prompt(f"Please choose a PC player-type: {''.join(names)}")

                    chosen = get_input()
                    if not chosen:
                        pos.print_output("Defaulting to 'simple'.")
                        input()
                        break

                    if chosen.strip().lower() in players.playstyles:
                        players.autoplay.playstyle = chosen
                        pos.print_output(f"`{players.autoplay.name}` playstyle set to {players.autoplay.playstyle}.")
                        break

            else:
                pos.print_prompt("Enter the name for Player 2: ")
                player2 = get_input()

                if not player2:
                    pos.print_output(f"Defaulting to `player_2`. Press 'enter'")
                    input()
                    player2 = "player_2"
                    pos.print_output(" ", clear=True)
                    break
                else:
                    if check_names:
                        pos.print_prompt(f"Is this correct? `{player2}`")
                        test = get_input()
                        if (test and test.lower() in ("y", "yes")) or not test:
                            break

    return player1, player2

def print_rules():
    clear_screen()
    rules = "SCORING: \n\nA `straight` (`1, 2, 3, 4, 5, 6`) is 1500 points\nA `small straight` (either `1, 2, 3, 4, 5` or `2, 3, 4, 5, 6`) is 750 points\n" \
    "Three-of-a-kind is `number x 100` (eg `3, 3, 3` is 300 points.)\nFour of a kind is `2x number x 100` (eg `3, 3, 3, 3` is 600 points)\n\n" \
    "1's and 5's are special: All other numbers are only valuable as part of one of the combinations above, and cannot be chosen alone.\n" \
    "But -- a 1 on its own is 100 points, and a 5 on its own is worth 50 points. \n\n" \
    "* 1's are extra special: instead of 'number x 100', they are 'number x 1000' - 1, 1, 1, 1 is 2000 points.\n\n" \
    "You must select at least one die each roll. If there is no valid die to select, you will bust, ending your turn and losing your points from that turn.\n" \
    "After selecting one or more die, you can choose to keep the points from those dice, or reroll the dice left over to try to get more points.\n\n" \
    "First player to 4000 points wins!\n\n[Press any key to return to Farkle.]"
    pos.print_points(rules, delay=True)
    input()
    clear_screen()


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

        if test and "1" in test or "2" in test:
            if "1" in test:
                single_player = True
            else:
                single_player = False
            break

    global players
    players = playerClass()

    pick_player_names(single_player)

    import os
    os.system("cls")

    while True:
        #print(HIDE)
        players.total_turns += 1
        if play_turn(players.current):
            print_wins()

            pos.print_prompt("Do you want to play again?")
            if players.autoplay and isinstance(players.autoplay, bool): # only autoplay next round if both players are PC
                test = "yes"
            else:
                test = get_input()
                #pos.print_input("        >> ")

            if (test and ("n" in test.lower() or "no" in test.lower())) or not test:
                pos.print_output(f"Alright, goodbye!")
                print("\n\n\n\n")
                break
        else:
            update_tally()
        players.switch_players()

main()

"""
need to:
DONE- hide the cursor when it's 'rolling' the dice.
DONE- get the positions worked out so it's not a scrolling screen but a static one.
DONE- set up the end of game properly, with score-clearing etc.
kinda done if it counts as a ui - maybe a basic ui, would be very handy for this.
DONE- need to add per-roll scoring, so it doesn't add single 1s together to get a three-of-a-kind etc. --  - sometimes the scores are wrong, I think perhaps this isn't /entirely/ fixed.
DONE- also need to be able to make sure singles aren't taken from straights. Only had this issue in the autoplay so far but it's annoying.
DONE- clear the tally after a round ends.
spacing fixed, timing still needs work - fix the spacing/timing on some of the print lines.
 - Want to add different ai behaviour. So, more strategic, more aggressive, etc.
 - I'm pretty sure I can use def auto_best(self) to do the calculations for active play/non-autoplay. It's extremely silly having two (or three, depending how you count it) fns for that part.
 - Still need to add the 'reroll all'.


Working on some refinements.
Currently the actual-player printing is wrong, it includes all possible matches, not just those chosen. The turn score is accurate though, it's just annoying and makes the record less useful.
I'm not sure how it's wrong like this though, because when it's using the fn for actual player it's meant to be getting its potential options from
    die_set = set(i for i in dice.dice if not i.used and i.held)
which doesn't include those.
Oh wait - no, that's not the issue. It's that it's using the nice already used by the straight a second time.

- Now accepts combinations of straights + single correctly.
Also, 55555 now gives 1050 points, as other than 1's, 5 of a kind is just 4 of a kind + 1.
"""
