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

    def __repr__(self):
        return (f"{self.dice_line}: dice // {self.prompt_line}: prompt // {self.input_line}: inputstr // {self.output_line}: output")

    """
    layout:

    error_lines = 4 lines designated for other printing, either above or below the following. Used for log prints so I don't have to externalise them. Maybe.

    dice_line   [  1  ]      [  1  ]      [  1  ]      [  1  ]      [  1  ]      [  1  ]

    prompt_line ["enter what you want to hold" / "do you want to take this score or roll again"]

    input_line ____

    output_line ['Scoring... ' / 'if you take, you will get x points' / 'ended the round with x points' / 'BUST!']
    """


    """self.position_str = str(positions)
        self.pos:dict = dict()
        import re
        last_pos = 0
        for i in range(1, 7):
            last_pos = self.position_str.find(str("["), last_pos)
    self.pos.setdefault(i, last_pos)
    #self.pos.setdefault(i, self.position_str.find(str(i), last_pos))
    print(f"self.pos: {self.pos}")"""


def make_play_area():

    import os
    os.system("cls")

     # reports current cursor position

    #print("\033[s", end='')
    #print("\033[6n", end='')

    #error_lines = list(str(i) for i in range(1,6))
    error_line = "2"
    error = f"\033[{int(error_line)};1f"
    start_line = "5" # before this is space for errors

    # this is now how much it adds to error line, not the actual line no.
    points = f"\033[{int(start_line)};1f"
    dice_str = f"\033[{int(start_line) + 3};1f"
    prompt = f"\033[{int(start_line) + 6};1f"
    inputstr = f"\033[{int(start_line) + 8};1f"
    output = f"\033[{int(start_line) + 10};1f"

    global pos
    pos = pos_data(error, points, dice_str, prompt, inputstr, output)

    #print(f"POS:\n{pos}")
    print(f"{pos.error_line} ERROR_LINE")
    print(f"{pos.points_line} POINTS LINE")
    print(f"{pos.dice_line} DICE LINE")
    print(f"{pos.prompt_line} PROMPT LINE")
    print(f"{pos.input_line} INPUT LINE")
    print(f"{pos.output_line} OUTPUT LINE")
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

    def print_updated(self, die = None, is_repeat = False):

        if is_repeat:
            MOVE_UP = "\033[2A" # moves cursor up one line, so the next print will overwrite the previous line. ~~animation~~
        else:
            MOVE_UP = ""
        print(MOVE_UP, end='')
        skin = die.skin if die and die.skin else self.skin if self.skin else colours.get("red")
        for i in range(1, 7):
            die = self.by_no[i]
            die_skin = colours[skin] if colours.get(skin) else skin # should allow for per-die skin, as well as default skin (which can be set by dice set on init or by player)
            if die.held:
                die_skin = colours.get("green") # green for held dice
                die_skin = "\033[2m" + die_skin # dim the held dice a bit to make them more visually distinct from unheld dice
            elif die.used:
                die_skin = colours.get("yellow")
            #else:
                #die_skin = colours.get("red") # red for unheld dice
            print(die_skin, f"   [  {die.value}  ]   " , str(END), end="")

        print("\n")

    def set_default_val(self):

        val = 1
        for die in dice.dice:
            if dice.skin and (not die.skin or die.skin == "default" or die.skin != dice.skin):
                die.skin = dice.skin

            die.place_no = die.value = val # place 1-6 in that order
            val += 1

    def auto_best(self):
        print("\nAUTO_BEST")
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
            print(f"VALS: {vals}")
            small_straight = list(i for i in (1, 2, 3, 4, 5) if i in vals)
            if not small_straight or (small_straight and len(small_straight) < 5):
                small_straight = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            if small_straight and len(small_straight) == 5:
                used_dice.add(i for i in die_set if i.value in small_straight and i not in used_dice)
            #if all(i for i in ("1", "2", "3", "4", "5") if i in vals) or all(i for i in vals in ("2", "3", "4", "5", "6")):
                matches["small straight"] = ({"small_straight": {1: 750}})


        for item in vals:
            count = sum(1 for die in die_set if die.value == item)
            if count >= 3:
                if item == 1:
                    used_dice.update(i for i in die_set if i not in used_dice and i.value == item)
                    matches["three (or four) of a kind"] = ({item: {count: int(1000 * (2 ** (count - 3)))}})
                else:
                    used_dice.update(i for i in die_set if i not in used_dice and i.value == item)
                    matches["three (or four) of a kind"] = ({item: {count: int(item * 100 * (2 ** (count - 3)))}})
            else:
                if item == 1:
                    used_dice.update(i for i in die_set if i not in used_dice and i.value == item)
                    matches["single ones"] = ({item: {count: int(100 * count)}})
                elif item == 5:
                    used_dice.update(i for i in die_set if i not in used_dice and i.value == item)
                    matches["single fives"] = ({item: {count: int(50 * count)}})


        print(f"MATCHES: {matches}")
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
            print(f"Best option: `{best_option}`{extra} for {best_value} points.")

        if not matches:
            print("BUST! Ending turn.")
            return False, None

        else:
            return matches, used_dice#best_value


    def dice_potential(self, starting=False):
        print("\nDICE POTENTIAL")
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
            print(f"VALS: {vals}")
            small_straight = list(i for i in (1, 2, 3, 4, 5) if i in vals)
            if not small_straight or (small_straight and len(small_straight) < 5):
                small_straight = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            if small_straight and len(small_straight) == 5:
            #if all(i for i in ("1", "2", "3", "4", "5") if i in vals) or all(i for i in vals in ("2", "3", "4", "5", "6")):
                matches["small straight"] = ({item: {count: 750}})

        print(f"MATCHES: {matches}")
        if matches:
            best_option = None
            best_value = 0
            for category in matches:
                for item, value in matches[category].items():
                    count, value = list(value.items())[0]
                    if value > best_value:
                        best_value = value
                        best_option = category
                        print(f"CATEGORY: {best_option}")
                        if "house" in best_option or "straight" in best_option:
                            extra = ''
                        else:
                            extra = f" with {count} {item}'s"
                    elif value == best_value:
                        best_option = best_option + " / " + category
            print(f"Best option: `{best_option}`{extra} for {best_value} points.")

        if not matches:
            if starting:
                print("BUST! Ending turn.")
                return False
            else:
                print("No matches but not starting. Should this bust too?")
        else:
            return matches#best_value

        return True

    def roll(self):
        from time import sleep
        import random
        count = 0
        print(HIDE, end='')
        self.print_updated(is_repeat=True)
        while count < 4:
            for die in self.dice:
                if not die.held and not die.used:
                    die.value = random.randint(1, 6)
                    self.print_updated(is_repeat=True)
                    sleep(0.01)

            #self.print_updated(is_repeat=True if count != 0 else False)
            sleep(0.1)
            count += 1
        self.print_updated(is_repeat=True)
        sleep(0.1)
        print(SHOW, end='')

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
        self.print_updated(is_repeat=True)

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

class playerClass:

    def __init__(self):
        self.players:set = set()
        self.current:playerInst = None
        self.opponent:playerInst = None

    def __repr__(self):
        return f"Players: {self.players} Current player: {self.current.name}"


def init_classes(player1 = "player_1", player2 = "player_2", player1_col = "red", player2_col = "blue"):

    global players
    players = playerClass()

    player_1 = playerInst(player1, skin=player1_col)
    players.players.add(player_1)
    players.current = player_1

    player_2 = playerInst(player2, skin=player2_col)
    players.players.add(player_2)
    players.opponent = player_2

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
    print(f"VALS SELECTED: {vals}")
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
            print("matched 1-5")
#        if (all("1", "2", "3", "4", "5") in vals):
            held_score += 750
        else:
            matched = list(i for i in (2, 3, 4, 5, 6) if i in vals)
            if matched:
                print("matched 2-6")
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
                print("item == 1")
                used_dice.update(set(i for i in dice_selection if i.value == item and i not in used_dice))
                held_score += 100 * count
            elif item == 5:
                print("item == 5")
                used_dice.update(set(i for i in dice_selection if i.value == item and i not in used_dice))
                held_score += 50 * count

    print(f"{player.name} can score {held_score} points with this roll. (If they choose to take the points, they will end their turn with a score of {player.game_score + player.turn_score + held_score}.)")
    player.turn_score += held_score
    return held_score, used_dice

def clear_held_and_used():

    for die in dice.dice:
        die.used = False
        die.held = False
        if die in dice.held_dice:
            dice.held_dice.remove(die)

def round_over(winner:playerInst):
    print(f"Round over! {winner.name} wins with a score of {winner.game_score}!")
    winner.wins += 1
    for playmate in players.values():
        if playmate != winner:
            playmate.losses += 1
            break
    clear_held_and_used()

    for player in (winner, playmate):
        player.game_score = 0
        player.turn_score = 0
        player.turn_count = 0

    return

def end_turn(player:playerInst):

    clear_held_and_used()
    print(f"Player.turn_score: {player.turn_score}")
    print(f"Player {player.name} ends their turn with a score of {player.game_score}")
    if player.game_score > 4000:
        round_over(winner=player)
        #for playmate in players.values():
            #if playmate != player:
                #playmate.losses += 1
    # have to mark the loss for other player, as well as clear held die etc.
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
    print(f"USED: `{used}`")
    if used and len(used) == 6:
        print("All dice used, resetting for next roll.")
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
        has_potential, used_dice = dice.auto_best()
        print(f"top of True for autoplay:\nHAS POTENTIAL: {has_potential} \nUSED DICE: {used_dice}\n")
        #has_potential = dice.dice_potential(starting=True)
        if not has_potential:
            #player.game_score = 0#+= player.turn_score
            player.turn_score = 0
            clear_held_and_used()
            return

        for i in used_dice:
            i.held = True

        dice.print_updated(is_repeat=True)

        score, used_dice = get_score(player, used_dice)

        mark_used(used_dice)

        used_dice_count = sum(1 for d in dice.dice if d.used)

        dice.print_updated(is_repeat=False)

        if used_dice_count < 4:
            print(f"length of used dice is less than 4? {used_dice_count}")
            #player.turn_score += score
            do_roll()
            print("Roll done, checking for potential...")
        else:
            #player.turn_score += score
            return take_roll(player)


def play_turn(player:playerInst):

    opponent = players.opponent
    print(f"{pos.error_line}OPPONENT: {opponent} / name: {opponent}")

    #print(f"set die to defaults for player {player.name}")
    if player.skin:
        dice.skin = player.skin
    else:
        dice.skin = ""
    player.turn_count += 1
    print(f"{pos.points_line} Current turn: {player.turn_count}  Current player: {player.name}. {player.name} has {player.game_score} points. Opponent has {opponent.game_score} points")
    print(f"{pos.output_line}{player.name} is rolling...")
    dice.set_default_val()
    dice.roll()

    """
    turn_score = int used holding the score of a single turn,  without considering past turns in this game.
    game_score = int used for holding player score for the current game, adding each turn_score when the held dice are added.
    """
    in_loop = set()
    while True:
        if player == players.get("player_2"):
            autoplay(player)
            #if player.game_score > 4000:
                #round_over(winner=player)
            return
        has_potential = dice.dice_potential(starting=True)
        if not has_potential:
            #player.game_score = 0#+= player.turn_score
            player.turn_score = 0
            clear_held_and_used()
            return

        used_dice = [die for die in dice.dice if die.used]
        #in_loop = set()
        if len(used_dice) == 6:#) or (has_potential and (used_dice)):# or dice.held_dice)):
            test = None
        else:
            print("Enter the values of the dice you want to hold. (You can enter multiple values separated by spaces.)")
            test = input(">> ")
        if test:
            #if "roll" in test:
            #    do_roll(in_loop)
            #if "take" in test:
            #    take_roll(player, turn_score)
            #    return

            for i, val in enumerate(test.strip().split(" ")):
                if not val:
                    continue
                try:
                    in_loop = get_dice_by_val(i, val, player, in_loop)
                except ValueError as e:
                    print(e)
            dice.print_updated(is_repeat=True)

        else:
            if has_potential:
                print(f"has_potential: {has_potential} type: {type(has_potential)}")

            print(f"Getting score...")
            mark_used(in_loop)

            dice.print_updated(is_repeat=True)
            get_score(player)
            test = True
            while test:
                test = input("Do you want to take the points, or continue rolling? (enter `take` or `roll`)\n>> ")
                if test.lower() == "take":
                    return take_roll(player)

                elif test.lower() == "roll":
                    do_roll()
                    break
                else:
                    print("Invalid input, please enter `take` or `roll`.")



def main():

    make_play_area()

    #for name in ["player_1", "player_2"]: # later can set player names. Just testing for now.
        #print(f"player: {playerInst(name)}\n")

    init_classes(player1 = "player_1", player2 = "player_2", player1_col = "red", player2_col = "blue")

    player_1 = True
    while True:
        if play_turn(players.current):
            print(f"{pos.prompt_line}Do you want to play again?", end='')
            print(pos.input_line, end='')
            test = input()
            if (test and ("n" in test.lower() or "no" in test.lower())) or not test:
                print(f"{pos.output_line}\nAlright, goodbye!\n\n\n\n")
                break
        player_1 = not player_1


main()
#make_play_area()
"""
need to:
DONE- hide the cursor when it's 'rolling' the dice.
- get the positions worked out so it's not a scrolling screen but a static one.
DONE- set up the end of game properly, with score-clearing etc.
- maybe a basic ui, would be very handy for this.
DONE- need to add per-roll scoring, so it doesn't add single 1s together to get a three-of-a-kind etc.
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
