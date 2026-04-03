"""farkle.py // simple text farkle game"""

#positions = ["   [  1  ]   ", "   [  2  ]   ", "   [  3  ]   ", "   [  4  ]   ", "   [  5  ]   ", "   [  6  ]   "]
positions = "   [  1  ]      [  2  ]      [  3  ]      [  4  ]      [  5  ]      [  6  ]   "
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

        self.lines = size.lines - 2 # for clearing full terminal

        self.tally = str(int((str(self.output_line).split("[")[1].split(";")[0])) + 3)
        self.tally_orig = int(self.tally) + 5
        self.dice_pos:dict[int, int] = {} # place_number: position in string

        last_pos = 0

        for i in range(1, 7):
            last_pos = positions.find(str("["), last_pos + 1)
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
        print(text)


    def print_points(self, text):

        text = self.points_line + text + self.clearline + END
        print(text, end = '')


    def print_dice(self, text='', die=None, skin=''):

        skin = colours[skin] if colours.get(skin) else skin
        #print(HIDE, end='')
        if die:
            #print(f"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nprint dice line: {self.dice_line.replace('\033', '')}")#\nPrinting dice for die at position {die.place_no} using\nself.dice_pos.get(die.place_no): {self.dice_pos.get(die.place_no)}")
            temp = self.dice_line.replace("7f", f"{self.dice_pos.get(die.place_no) + 7}f")

        if isinstance(text, list):
            text = ''.join(text)

        if die:
            text = temp + skin + text + END
        else:
            text = self.dice_line + text
        print(text, end = '')

    def print_prompt(self, text):

        text = self.prompt_line + text + self.clearline + END
        print(text, end = '')


    def print_input(self, text):

        print(f"{self.input_line}", end='')
        #print("\033[0J")
        text = self.input_line + text + self.clearline + END
        print(text, end = '')


    def print_output(self, text):
        print(f"{self.output_line}{self.clearline}")#self.output_line + text + self.clearline + END)
        text = self.output_line + "\033[2;36m"+ "  [  " + text + "  ]" + END
        print(text)
        print(self.clearline, end='')
    """
    layout:

    error_lines = 4 lines designated for other printing, either above or below the following. Used for log prints so I don't have to externalise them. Maybe.

    dice_line   [  1  ]      [  1  ]      [  1  ]      [  1  ]      [  1  ]      [  1  ]

    prompt_line ["enter what you want to hold" / "do you want to take this score or roll again"]

    input_line ____

    output_line ['Scoring... ' / 'if you take, you will get x points' / 'ended the round with x points' / 'BUST!']
    """


    """self.position_str = str(positions)

    self.pos.setdefault(i, last_pos)
    #self.pos.setdefault(i, self.position_str.find(str(i), last_pos))
    print(f"self.pos: {self.pos}")"""


def make_play_area():

    import os
    os.system("cls")


    #print("\033[s", end='')
    #print("\033[6n", end='') # reports current cursor position

    #error_lines = list(str(i) for i in range(1,6))
    error_line = "0"
    error = f"\033[{int(error_line)};1f"
    start_line = "6" # before this is space for errors

    # this is now how much it adds to error line, not the actual line no.
    points = f"\033[{int(start_line)};1f\033[2;32m"
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
    print()

class die:
    def __init__(self, place_number = 1, skin=None):
        self.value = 1
        self.place_no = place_number
        self.held = False
        self.used = False #for dice that have been rolled and kept aside, to stop them being recounted and acted on thereafter.
        self.skin = skin

class dice_data:

    def __init__(self):

        self.skin = None
        self.dice:set[die] = set()
        self.by_no:dict[str, die] = {die.place_no: die for die in self.dice}
        self.held_dice:set[die] = set()

    def init_dice(self):

        for i in range(1, 7):
            self.dice.add(die(place_number=i, skin=self.skin))
        self.by_no = {die.place_no: die for die in self.dice}
        #for i in range(1, 7):
            #print(f"i: {i} // self.by_no[i]: {self.by_no[i]} ")

    def print_updated(self, die = None):

        def print_die(die):
            if isinstance(die, int):
                die = self.by_no[i]
            die_skin = die.skin if die.skin else colours.get("red") # should allow for per-die skin, as well as default skin (which can be set by dice set on init or by player)
            if die.held:
                die_skin = colours.get("green") # green for held dice
                die_skin = "\033[2m" + die_skin # dim the held dice a bit to make them more visually distinct from unheld dice
            elif die.used:
                die_skin = colours.get("yellow")
            #else:
                #die_skin = colours.get("red") # red for unheld dice
            pos.print_dice(text = f"[  {die.value}  ]", die=die, skin=die_skin)


        #if is_repeat:
        #    MOVE_UP = "\033[2A" # moves cursor up one line, so the next print will overwrite the previous line. ~~animation~~
        #else:
        #    MOVE_UP = ""
        #print(MOVE_UP, end='')
        #dice_printing = []
        #skin = die.skin if die and die.skin else self.skin if self.skin else colours.get("red")
        if not die:
            for i in range(1, 7):
                print_die(i)

        else:
            print_die(die)
            #pos.print_dice(text = f"   [  {die.value}  ]", die=die, skin=die.skin)

            #print(f"{die_skin}   [  {die.value}  ]   ", end='')
        #pos.print_dice(dice_printing)


    def set_default_val(self):

        val = 1
        for die in dice.dice:
            if dice.skin and (not die.skin or die.skin == "default" or die.skin != dice.skin):
                die.skin = dice.skin

            die.place_no = die.value = val # place 1-6 in that order
            val += 1
        dice.print_updated()

    def auto_best(self):
        pos.print_error("AUTO_BEST")
        matches = {}
        used_dice = set()

        die_set = set(i for i in dice.dice if not i.used)
        vals = set(i.value for i in dice.dice if not i.used)

        if len(vals) == 6:
            for item in vals:
                count = sum(1 for die in die_set if die.value == item)
                if count == 6:
                    used_dice = die_set
                    matches["full house"] = ({1: {count: 1500}})
        elif len(vals) >= 5:
            pos.print_error(f"VALS: {vals}", 1)
            small_straight = list(i for i in (1, 2, 3, 4, 5) if i in vals)
            if not small_straight or (small_straight and len(small_straight) < 5):
                small_straight = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            if small_straight and len(small_straight) == 5:
                used_dice.update(set(i for i in die_set if i.value in small_straight and i not in used_dice))
            #if all(i for i in ("1", "2", "3", "4", "5") if i in vals) or all(i for i in vals in ("2", "3", "4", "5", "6")):
                matches["small straight"] = ({"small_straight": {1: 750}})


        for item in vals:
            count = sum(1 for die in die_set if die.value == item)
            if count >= 3:
                if item == 1:
                    used_dice.update(set(i for i in die_set if i not in used_dice and i.value == item))
                    matches["three (or four) of a kind"] = ({item: {count: int(1000 * (2 ** (count - 3)))}})
                else:
                    used_dice.update(set(i for i in die_set if i not in used_dice and i.value == item))
                    matches["three (or four) of a kind"] = ({item: {count: int(item * 100 * (2 ** (count - 3)))}})
            else:
                if item == 1:
                    used_dice.update(set(i for i in die_set if i not in used_dice and i.value == item))
                    matches["single ones"] = ({item: {count: int(100 * count)}})
                elif item == 5:
                    used_dice.update(set(i for i in die_set if i not in used_dice and i.value == item))
                    matches["single fives"] = ({item: {count: int(50 * count)}})


        pos.print_error(f"MATCHES: {matches}", 2)
        if matches:
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
                    elif value == best_value:
                        best_option = best_option + " / " + category
            pos.print_error(f"Best option: `{best_option}`{extra} for {best_value} points.", 3)

        if not matches:
            pos.print_output(f"BUST! Ending {players.current.name}'s turn.")
            from time import sleep
            sleep(.8)
            return False, None

        else:
            return matches, used_dice#best_value


    def dice_potential(self, starting=False):
        pos.print_error(f"DICE POTENTIAL")
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
            pos.print_error(f"VALS: {vals}", 1)
            small_straight = list(i for i in (1, 2, 3, 4, 5) if i in vals)
            if not small_straight or (small_straight and len(small_straight) < 5):
                small_straight = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            if small_straight and len(small_straight) == 5:
            #if all(i for i in ("1", "2", "3", "4", "5") if i in vals) or all(i for i in vals in ("2", "3", "4", "5", "6")):
                matches["small straight"] = ({item: {count: 750}})

        pos.print_error(f"MATCHES: {matches}", 2)
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
            pos.print_error(f"Best option: `{best_option}`{extra} for {best_value} points.", 3)

        if not matches:
            if starting:
                pos.print_output("BUST! Ending turn.")
                from time import sleep
                sleep(.8)
                return False
            else:
                print(f"{pos.output_line}No matches but not starting. Should this bust too?")
        else:
            return matches#best_value

        return True

    def roll(self):
        from time import sleep
        import random
        count = 0
        for die in self.dice:
            self.print_updated(die)
        while count < 4:
            for die in self.dice:
                if not die.held and not die.used:
                    die.value = random.randint(1, 6)
                    sleep(0.015)
                    self.print_updated(die)
            #self.print_updated( if count != 0 else False)
                sleep(0.02)

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

    def __repr__(self):
        return f"[(player: {self.name} // held_score: {self.held_dice} // turn_score: {self.turn_score})]"

def clear_screen(limited=False):
    from time import sleep
    sleep(.3)
    print(f"\033[H{HIDE}", end='')
    for i in range(pos.lines):
        if limited == True:
            if f"[{i-1};" in pos.output_line:
                break

        #if f"[{i};" in pos.output_line:
        print("\033[2K")
        sleep(0.05)
    #pos.print_dice(text=" "* len(positions))
    sleep(.3)

class playerClass:

    def __init__(self):
        self.players:set = set()
        self.current:playerInst = None
        self.opponent:playerInst = None
        self.autoplay = True

        self.total_turns:int = int()
        self.tally:dict[int, str] = {}

    def __repr__(self):
        return f"Players: {self.players} Current player: {self.current.name}"

    def switch_players(self):
        self.current, self.opponent = self.opponent, self.current
        clear_screen(limited=True)
        from time import sleep
        sleep(.3)



def init_classes(player1 = "player_1", player2 = "player_2", player1_col = "red", player2_col = "blue", single_player=True):

    global players
    players = playerClass()

    player_1 = playerInst(player1, skin=player1_col)
    players.players.add(player_1)
    players.current = player_1

    player_2 = playerInst(player2, skin=player2_col)
    players.players.add(player_2)
    players.opponent = player_2

    if single_player == True:
        players.autoplay = player_2

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

def get_score(player, autoplay_dice=None):
    if autoplay_dice:
        dice_selection = set(autoplay_dice)
    else:
        dice_selection = dice.held_dice
    held_score = 0
    vals = set(i.value for i in dice_selection)

    used_dice = set()
    if len(vals) == 6:
        for item in vals:
            count = sum(1 for die in dice_selection if die.value == item)
            if count == 6:
                used_dice = dice_selection
        held_score += 1500

    elif len(vals) == 5:
        matched = list(i for i in (1, 2, 3, 4, 5) if i in vals)
        if matched and len(matched) == 5:
            pos.print_error(f"matched 1-5")
#        if (all("1", "2", "3", "4", "5") in vals):
        else:
            matched = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            if matched:
                pos.print_error(f"matched 2-6")
        if matched and len(matched) == 5:
            used_dice.update(set(i for i in dice_selection if len(used_dice) < 5 and i.value in vals and i not in used_dice))#(2, 3, 4, 5, 6) if i in vals)#die for die in dice_selection if die.value == item and die not in used_dice)
        #elif (all("2", "3", "4", "5", "6") in vals):
            held_score += 750

    for item in vals:
        count = sum(1 for die in dice_selection if die.value == item and die not in used_dice)
        if count >= 3:
            used_dice.update(set(die for die in dice_selection if die.value == item and die not in used_dice))
            if item == 1:
                held_score += 1000 * (2 ** (count - 3))
            else:
                held_score += item * 100 * (2 ** (count - 3))
        elif count:
            if item == 1:
                pos.print_error(f"item == 1", 1)
                used_dice.update(set(i for i in dice_selection if i.value == item and i not in used_dice))
                held_score += 100 * count
            elif item == 5:
                pos.print_error(f"item == 5", 2)
                used_dice.update(set(i for i in dice_selection if i.value == item and i not in used_dice))
                held_score += 50 * count

    pos.print_output(f"{player.name} can score {held_score} points here if they choose to take the points, taking their total score to {player.game_score + player.turn_score + held_score}.")
    player.turn_score += held_score
    return held_score, used_dice

def clear_held_and_used():

    for die in dice.dice:
        die.used = False
        die.held = False
        if die in dice.held_dice:
            dice.held_dice.remove(die)

def round_over(winner:playerInst):
    pos.print_output(f"Round over! {winner.name} wins with a score of {winner.game_score}!")
    from time import sleep
    sleep(.8)
    winner.wins += 1
    players.opponent.losses += 1
    clear_held_and_used()

    for player in (winner, players.opponent):
        player.game_score = 0
        player.turn_score = 0
        player.turn_count = 0
    players.total_turns = 0

    return

def update_tally():
    pos.print_error(f"updating tally for {players.current.name}")
    #print(fr"{pos.tally_orig} in str(pos.tally): {True if pos.tally_orig in pos.tally else False}")
    players.tally[players.total_turns] = (players.current.name, players.current.game_score)
    count = int(pos.tally)
    column = 4
    print(HIDE, end='')
    for i, entry in players.tally.items():
        #print(f"ENTRY: {entry} / type: {type(entry)}")
        name, score = entry
        #print(f"NAME: {name} SCORE: {score}")
        if count == pos.tally_orig:
            count = int(pos.tally)
            column = column + 32
        print(f"\033[{count};{column}f\033[2;32mTurn {i}: {name} = {score}")
        count = count + 1
        pos.print_error(f"printed tally for {players.current.name} at count {count}, column {column}", 2)
    print(END, end='')


def end_turn(player:playerInst):

    clear_held_and_used()
    pos.print_output(f"Player {player.name} ends their turn with a score of {player.game_score}.")
    from time import sleep
    sleep(.8)
    if player.game_score > 4000:
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

    #mark_used(in_loop)
    dice.roll()

def take_roll(player:playerInst):

    player.game_score += player.turn_score
    if end_turn(player):
        return "game over"

def autoplay(player:playerInst):
    """for player_2 to be PC controlled. super basic."""

    while True:
        dice.print_updated()
        pos.print_output("Getting score...")
        has_potential, used_dice = dice.auto_best()
        pos.print_error(f"HAS POTENTIAL: {has_potential}")# USED DICE: {used_dice}")
        #has_potential = dice.dice_potential(starting=True)
        if not has_potential:
            #player.game_score = 0#+= player.turn_score
            player.turn_score = 0
            clear_held_and_used()
            return end_turn(player)

        for i in used_dice:
            i.held = True

        dice.print_updated()
        from time import sleep
        sleep(.4)
        score, used_dice = get_score(player, used_dice)

        mark_used(used_dice)
        sleep(.4)

        used_dice_count = sum(1 for d in dice.dice if d.used)

        dice.print_updated()

        sleep(.8)
        if used_dice_count < 4:
            #player.turn_score += score
            do_roll()
            pos.print_output("Roll done, checking for potential...")
        else:
            sleep(.5)
            #player.turn_score += score
            return take_roll(player)


def play_turn(player:playerInst):

    opponent = players.opponent
    #print(f"{pos.error_line}OPPONENT: {opponent} / name: {opponent}")

    #print(f"set die to defaults for player {player.name}")
    if player.skin:
        dice.skin = player.skin
    else:
        dice.skin = ""
    player.turn_count += 1
    pos.print_points(f"        Current turn: {player.turn_count}  Current player: {player.name}. {player.name} has {player.game_score} points. Opponent has {opponent.game_score} points.")
    pos.print_output(f"{player.name} is rolling...")
    dice.set_default_val()
    dice.print_updated()
    #from time import sleep
    #sleep(0.2)
    dice.roll()

    """
    turn_score = int used holding the score of a single turn,  without considering past turns in this game.
    game_score = int used for holding player score for the current game, adding each turn_score when the held dice are added.
    """
    in_loop = set()
    while True:
        if players.autoplay:# and player == players.autoplay:
            return autoplay(player)

        has_potential = dice.dice_potential(starting=True)
        if not has_potential:
            player.turn_score = 0
            clear_held_and_used()
            return

        used_dice = [die for die in dice.dice if die.used]
        #in_loop = set()
        if len(used_dice) == 6:
            test = None
        else:
            pos.print_prompt("Enter the values of the dice you want to hold. (You can enter multiple values separated by spaces.)")
            pos.print_input(f">> {SHOW}")
            test = input()
        if test:

            for i, val in enumerate(test.strip().split(" ")):
                if not val:
                    continue
                try:
                    in_loop = get_dice_by_val(i, val, player, in_loop)
                except ValueError as e:
                    pos.print_error(e)
            dice.print_updated()

        else:
            if has_potential:
                pos.print_error(f"has_potential: {has_potential} type: {type(has_potential)}")

            pos.print_output(f"{pos.output_line}Getting score...")
            mark_used(in_loop)

            dice.print_updated()
            get_score(player)

            while True:
                pos.print_prompt(f"Do you want to take the points, or continue rolling? (enter `take` or `roll`)")
                pos.print_input(">> ")
                test = input()
                if test.lower() in ("take", "t"):
                    return take_roll(player)

                elif test.lower() in ("roll", "r"):
                    do_roll()
                    break
                else:
                    pos.print_error("Invalid input, please enter `take` or `roll`.")

def print_wins():
    pos.print_prompt(f"        {players.current.name} has won {players.current.wins} game(s).  {players.opponent.name} has one {players.opponent.wins} game(s).")

def main():

    make_play_area()

    #for name in ["player_1", "player_2"]: # later can set player names. Just testing for now.
        #print(f"player: {playerInst(name)}\n")

    init_classes(player1 = "player_1", player2 = "player_2", player1_col = "red", player2_col = "blue")

    while True:
        players.total_turns += 1
        if play_turn(players.current):
            pos.print_prompt("Do you want to play again?")
            if players.autoplay and isinstance(players.autoplay, bool):
                test = "yes"
            else:
                pos.print_input(">> ")
                test = input()
            if (test and ("n" in test.lower() or "no" in test.lower())) or not test:
                pos.print_output(f"Alright, goodbye!\n\n\n\n")
                break
            if test:
                clear_screen()
                print_wins()
        else:
            update_tally()
        players.switch_players()
        from time import sleep
        sleep(0.5)
        pos.print_output(f"Switching players, next up is {players.current.name}...")
        sleep(1)



main()
#make_play_area()
"""
need to:
DONE- hide the cursor when it's 'rolling' the dice.
- get the positions worked out so it's not a scrolling screen but a static one.
DONE- set up the end of game properly, with score-clearing etc.
- maybe a basic ui, would be very handy for this.
DONE- need to add per-roll scoring, so it doesn't add single 1s together to get a three-of-a-kind etc. --  - sometimes the scores are wrong, I think perhaps this isn't /entirely/ fixed.
DONE- also need to be able to make sure singles aren't taken from straights. Only had this issue in the autoplay so far but it's annoying.
"""

"""
layout:

diceline   [  1  ]      [  1  ]      [  1  ]      [  1  ]      [  1  ]      [  1  ]

after printing diceline, run
`ESC[0J`
to clear the following lines each time.

printline ["enter what you want to hold" / "do you want to take this score or roll again"]

inputline ____

outputline ['Scoring... ' / 'if you take, you will get x points' / 'ended the round with x points' / 'BUST!']
"""
