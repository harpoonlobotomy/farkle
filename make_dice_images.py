
"""
WHAT IS WHERE:
'BASE' is all the grey/default gifs.
* BASE/farkle is letter_to_blank and blank_to_letter = the letter portion has the farkle colour applied, the blank doesn't, so it can have the player colour applied for playerdice<>farkle transitions.
* BASE/self_roll is just one complete roll of that character.
* BASE/from_x_to_y is each die value to each other die value, + to and from blank.

'blanks' is components that make the above gifs. The raw blank frames, characters and face masks.

'num_by_colour' is custom-coloured versions of those found in BASE; each folder is named for a colour. Will need to add a button to clear old die colours soon.

Each of these is only small, 11 frames long. The intent is to combine them - at startup/player colour change we make the coloured variants from BASE, then as needed combine those portions into continuous rolls.
Currently the plan is to make gifs on the fly, but perhaps playing the gifs one after the other would work. The challenge is getting the gifs to play, so for now I'll pre-compile them.

"""

from PIL import Image, ImageChops
import os

class img_class:
    def __init__(self):
        self.output_dir = f"{os.getcwd()}\\dice_graphics\\"
        self.settings_file = f"{os.getcwd()}\\farkle_settings.json"

        import json
        with open(self.settings_file) as f:
            settings = json.load(f)

        font = settings["user_set"]["die_face_font"] if settings["user_set"].get("die_face_font") else settings["defaults"]["die_face_font"]
        self.chars_dir = f"{self.output_dir}blanks\\chars_blanks\\{font}\\"
        if not os.path.isdir(self.chars_dir):
            print(f"No font found for {font}. Using standard instead.")
            self.chars_dir = f"{self.output_dir}blanks\\chars_blanks\\standard\\"

        self.chars_blanks = os.listdir(self.chars_dir)

        self.frame_dir = f"{self.output_dir}blanks\\frame_blanks\\"
        self.frame_blanks = os.listdir(self.frame_dir)

        self.frame_mask_dir = f"{self.output_dir}blanks\\face_masks\\"
        self.frame_mask_files = os.listdir(self.frame_mask_dir)

        self.standard_dice_colour = "#11D49A"
        self.bust_colour = "#330303"

        self.button_held = "#F8DC5E"
        self.button_used = "#666354"

        self.effect_layers = settings["user_set"]["effect_layers"] if settings["user_set"].get("effect_layers") else settings["defaults"]["effect_layers"]

        self.effect_dir = f"{self.output_dir}effect_layers\\"

        self.rotate_counter = 0

        if not os.path.isdir(self.effect_dir):
            print("No effect dir.")
            self.effect_files = []
        else:
            self.effect_files = os.listdir(self.effect_dir) # Not folders - I only need a single image for each if we're just applying it as a rotation and not replacing the full blank.
            if self.effect_files:
                print(f"All effect files: {self.effect_files} // effect_layers: {self.effect_layers}")
                print(list(i for i in self.effect_files))
                self.effect_files = list(i for i in self.effect_files if i.replace(".png", "") in self.effect_layers) # allows for layering
            print(f"effect files if i in effect_layers: {self.effect_files}")

        self.movement = {
            "outgoing": { ## how many pixels down on 7 from 0 (final y position, not additive per frame.)
                    "01":6,
                    "02":14,
                    "03":24,
                    "04":40,
                    "05":52,
                    "06":63,
                    },
            "incoming":
                {
                    "04": -75,
                    "05": -64,
                    "06": -53,
                    "07": -38,
                    "08": -28,
                    "09": -16,
                    "10": -6,
                    "11": 0
                }
        }

        self.fark_colours = {
                    "f": "#db270d",
                    "a": "#ffb302",
                    "r": "#71b335",
                    "k": "#4e8f9a",
                    "l": "#4e5b9a",
                    "e": "#ae3aad"
                }


img = img_class()

class output_used_filepaths:
    def __init__(self):
        self.used_filepaths:set = set()

    def update(self, path):
        self.used_filepaths.add(path)

    def save_data(self):
        output_file = f"{os.getcwd()}\\used_filepaths.json"
        filepaths = list(self.used_filepaths)
        import json
        with open(output_file, "w+") as f:
            json.dump(filepaths, f, indent=4)

o = output_used_filepaths()

def get_roll(outgoing=None, outgoing_colour=None, incoming=None, incoming_colour=None, anim_frames=[], recolour=None, make_frame_zero=False):

    do_update=True
    add_effect_layer=True

    if outgoing == "blank":
        outgoing_path = None
    else:
        #print(f"outgoing: {outgoing}")
        outgoing_path = list(i for i in img.chars_blanks if i == f"{str(outgoing)}.png")[0]

    if incoming == "blank":
        incoming_path = None
    else:
        #print(f"incoming: {incoming}")
        incoming_path = list(i for i in img.chars_blanks if i == f"{str(incoming)}.png")[0]

    if incoming and incoming in ("f", "a", "r", "k", "l", "e"):
        incoming_colour =img.fark_colours[incoming]
    elif incoming and incoming in ("d", "b", "u", "s", "t"):
        incoming_colour =img.bust_colour
    else:
        incoming_colour = incoming_colour if incoming_colour else recolour if recolour and isinstance(recolour, str) else img.standard_dice_colour # later this will be player colours

    if outgoing and outgoing in ("f", "a", "r", "k", "l", "e"):
        outgoing_colour =img.fark_colours[outgoing]
    elif outgoing and outgoing in ("d", "b", "u", "s", "t"):
        outgoing_colour =img.bust_colour
    else:
        outgoing_colour = outgoing_colour if outgoing_colour else recolour if recolour and isinstance(recolour, str) else img.standard_dice_colour

    outgoing_y_pos = None
    incoming_y_pos = None
    for filepath in sorted(img.frame_blanks):
        if filepath == "00.png":
            continue
        if make_frame_zero and filepath != "11.png": # frame zero is actually frame 11 but w/e, it'll work
            continue
        with Image.open(img.frame_dir + filepath) as f_blank:
            if do_update:
                o.update(img.frame_dir + filepath)
            frame_no = filepath.replace(".png", "")

            new = Image.new(mode="RGBA", size=f_blank.size)
            new.paste(f_blank)
            if outgoing_path:
                if do_update:
                    o.update(img.chars_dir + outgoing_path)

                with Image.open(img.chars_dir + outgoing_path) as out_img:
                    if frame_no in img.movement["outgoing"]:
                        outgoing_y_pos = img.movement["outgoing"][frame_no]
                        new.alpha_composite(out_img, (0,outgoing_y_pos))

            if incoming_path:
                if do_update:
                    o.update(img.chars_dir + incoming_path)

                with Image.open(img.chars_dir + incoming_path) as in_img:
                    if frame_no in img.movement["incoming"]:
                        incoming_y_pos = img.movement["incoming"][frame_no]
                        new.alpha_composite(in_img, (0,incoming_y_pos))

            """if add_effect_layer and img.effect_files: # TODO: Fix this so it applies to all frames correctly, currently it applies to the main face but not the underside. Need to investigate why.
                rotate_effects = True
                for effect in img.effect_files:
                    with Image.open(img.effect_dir + effect) as effect_img:
                        if rotate_effects:
                            effect_img = effect_img.rotate(90*img.rotate_counter)
                        if outgoing_path and frame_no in img.movement["outgoing"]:
                            outgoing_y_pos = img.movement["outgoing"][frame_no]
                            new.alpha_composite(effect_img, (0,outgoing_y_pos))
                        if incoming_path and frame_no in img.movement["incoming"]:
                            incoming_y_pos = img.movement["incoming"][frame_no]
                            new.alpha_composite(effect_img, (0,incoming_y_pos))"""

            if recolour or (incoming_colour and outgoing_colour):
                frame_mask = list(i for i in img.frame_mask_files if  i == filepath)
                if frame_mask:
                    frame_mask = frame_mask[0]
                    if do_update:
                        o.update(img.frame_mask_dir + frame_mask)
                else:
                    print(f"No frame mask found for {filepath}. All frame masks: \n{img.frame_mask_files}")

                new = recolour_frame(new, outgoing_colour, incoming_colour, img.frame_mask_dir + frame_mask)

            if make_frame_zero:
                directory = os.path.dirname(make_frame_zero)
                if not os.path.isdir(directory):
                    os.makedirs(directory)
                new.save(make_frame_zero)
                return None
            anim_frames.append(new)
    return anim_frames


def recolour_frame(image:Image.Image, outgoing_colour="blue", incoming_colour="red", frame_mask=None):
    """ Now allows str('None') as incoming/outgoing colour, to allow that portion to remain unchanged from the original."""

    image=image.convert("RGBA")
    if outgoing_colour == "None":
        new_image = image
    else:
        square = Image.new("RGBA", size=(100, 100), color=outgoing_colour)
        new_image = ImageChops.overlay(image, square)
        if outgoing_colour == incoming_colour:
            image
            new_image = new_image.convert("RGB")
            return new_image

    if incoming_colour == "None":
        alt_image = image
    else:
        alt_square = Image.new("RGBA", size=(100, 100), color=incoming_colour)
        alt_image = ImageChops.overlay(image, alt_square)


    alt_image = alt_image.convert("RGB")
    new_image = new_image.convert("RGB")
    with Image.open(frame_mask) as mask:
        mask = mask.convert("1")
        new_image.paste(alt_image, mask=mask)

    return new_image

def transition_to_from(anim_frames, outgoing_char, incoming_char, start_roll=True, blank_before_incoming=True, end_roll=True, output_name=None, start_from_blank=False, end_with_blank=False, recolour=None, continue_with_list=False, subfolder="BASE\\from_x_to_y\\", incoming_colour=None, outgoing_colour=None): # maybe set blank_before_incoming if char in FARKLE else false

    if not anim_frames:
        anim_frames = []

    if start_from_blank:
        anim_frames = get_roll(outgoing="blank", outgoing_colour=outgoing_colour, incoming=outgoing_char, incoming_colour=incoming_colour, anim_frames=anim_frames, recolour=recolour)

    if start_roll: # means we start with a full rotation of the outgoing
        anim_frames = get_roll(outgoing=outgoing_char, outgoing_colour=outgoing_colour, incoming=outgoing_char, incoming_colour=incoming_colour, anim_frames=anim_frames, recolour=recolour)

    if blank_before_incoming: # TODO: Could use this for the farkle anim, but would have to change the reroll to accomodate.
        anim_frames = get_roll(outgoing=outgoing_char, outgoing_colour=outgoing_colour, incoming="blank", incoming_colour=incoming_colour, anim_frames=anim_frames, recolour=recolour)
        anim_frames = get_roll(outgoing="blank", outgoing_colour=outgoing_colour, incoming=incoming_char, incoming_colour=incoming_colour, anim_frames=anim_frames, recolour=recolour)
    else:
        anim_frames = get_roll(outgoing=outgoing_char, outgoing_colour=outgoing_colour, incoming=incoming_char, incoming_colour=incoming_colour, anim_frames=anim_frames, recolour=recolour) # Added start_from_100 to this, as I think it's the only one that'll be applicable here. Setting this up for the autogeneration of farkle full roll.

    if end_roll:
        anim_frames = get_roll(outgoing=incoming_char, outgoing_colour=outgoing_colour, incoming=incoming_char, incoming_colour=incoming_colour, anim_frames=anim_frames, recolour=recolour)

    if end_with_blank:
        anim_frames = get_roll(outgoing=incoming_char, outgoing_colour=outgoing_colour, incoming="blank", incoming_colour=incoming_colour, anim_frames=anim_frames, recolour=recolour)

    if not output_name:
        output_name = outgoing_char

    if continue_with_list:
        return anim_frames # for chaining longer strings.

    if not os.path.isdir(f"{img.output_dir}{subfolder}\\"):
        os.makedirs(f"{img.output_dir}{subfolder}\\")
    anim_frames[0].save(img.output_dir + f"{subfolder}\\{output_name}.gif", append_images=anim_frames[1:], save_all=True, duration=50, optimise=False, loop=0)
    return []

fark_dict = {
    "f":"1",
    "a":"2",
    "r":"3",
    "k":"4",
    "l":"5",
    "e":"6",
}

def make_farkle_chain():

    make_farkle_chain = False#True

    if make_farkle_chain:
        anim_frames = []
        count = 0
        for k, char in fark_dict.items(): # through the whole lot
            if count:
                for _ in range(count):
                    anim_frames = get_roll(outgoing="blank", incoming="blank", anim_frames=anim_frames, recolour="farkle")

            anim_frames = transition_to_from(anim_frames, "blank", k, start_roll=True, blank_before_incoming=False, end_roll=True, output_name = f"farkle_chain_{k}_{char}", start_from_blank=True, end_with_blank=False, recolour="farkle", continue_with_list=False)
            count += 1


def make_combination_image(make_farkle = False, make_bust=False, make_other=None, make_other_colour = None, other_subfolder=None, end_blank=True, filename="temp", anim_frames=None): ## redo this to use a dict instead of listing them all out like this.

    def make_from_list(incoming_list, output_path, colour=None, subfolder=None, is_other=False, end_blank=True, anim_frames=None):
        ## For full roll for each letter before changing, set end_roll=True.
        if not anim_frames:
            anim_frames = []

        for i, key in enumerate(incoming_list):
            if i == len(incoming_list)-2: # is -2 so that the [i+1] lands on the last entry.
                anim_frames = transition_to_from(anim_frames, outgoing_char=key, incoming_char=incoming_list[i+1], start_roll=False, blank_before_incoming=False,
                        end_roll=False, output_name = output_path, start_from_blank=False, end_with_blank=end_blank, recolour=colour, continue_with_list=False, subfolder=subfolder)
            elif i < len(incoming_list) -1:
                anim_frames = transition_to_from(anim_frames, outgoing_char=key, incoming_char=incoming_list[i+1], start_roll=False, blank_before_incoming=False,
                        end_roll=False, output_name = output_path, start_from_blank=False, end_with_blank=False, recolour=colour, continue_with_list=True, subfolder=subfolder)

    farkle_list = ["blank", "f", "a", "r", "k", "l", "e"]#, "blank"] # no blank on the end so it stays on the e? Not sure what I want.
    bust_list = ["blank", "d", "b", "u", "s", "t", "d"]#, "blank"]
    if make_farkle:
        make_from_list(farkle_list, output_path = "farkle_all_in_one", colour="farkle")
    if make_bust:
        make_from_list(bust_list, output_path = "bust_all_in_one", colour="bust")
    if make_other:
        make_from_list(make_other, output_path = filename, colour=make_other_colour, subfolder = other_subfolder, end_blank=False, anim_frames=anim_frames) # is_other=True to add blank to start


def apply_colour_to_gif(base_image, outgoing_colour, incoming_colour, target_path):

    def modify_gif(im:Image.Image, outgoing_colour, incoming_colour, target_path):

        new = []
        for frame_num in range(im.n_frames):
            try:
                im.seek(frame_num)
                if outgoing_colour == incoming_colour:
                    frame_mask=None
                else:
                    mask_no = frame_num+1
                    if mask_no == 11:
                        mask_no = 0
                    if len(str(mask_no)) == 1:
                        str_num = f"0{mask_no}.png"
                    else:
                        str_num = f"{mask_no}.png"

                    frame_mask = list(i for i in img.frame_mask_files if i == str_num)
                if frame_mask:
                    frame_mask = img.frame_mask_dir + frame_mask[0]

                new_frame = recolour_frame(im, outgoing_colour, incoming_colour, frame_mask=frame_mask)
                new.append(new_frame)
            except Exception as e:
                print(f"Failed to seek for {frame_num} from n_frames: {im.n_frames}: {e}")

        new[0].save(target_path, append_images=new[1:], save_all=True)

        return

    with Image.open(base_image) as im:
        if "gif" in base_image:
            modify_gif(im, outgoing_colour, incoming_colour, target_path)

def colour_players_dice(player_colour, force_recolour=False, just_stills=False):


    output_path = img.output_dir + f"num_by_colour\\{player_colour}\\"

    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    elif not force_recolour:
        print(f"Directory for {output_path} already exists. Stopping. Set 'force_recolour' to force re-creation - can also be accessed by resetting to defaults in ingame settings.")
        return output_path

    make_single_frames(to_make="123456", set_colour=player_colour, output_dir=output_path)

    make_hold_and_used = False
    if make_hold_and_used:
        held_and_used()

    if just_stills: # Is always true for the moment, I don't use the blank_to_x anims.
        return

    for k in fark_dict:
        transition_to_from([], "blank", k, start_roll=False, blank_before_incoming=False, end_roll=False, output_name = f"blank_to_{k}", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=False, incoming_colour =img.fark_colours[k], outgoing_colour=player_colour, subfolder=f"num_by_colour\\{player_colour}\\")
        transition_to_from([], k, "blank", start_roll=False, blank_before_incoming=False, end_roll=False, output_name = f"{k}_to_blank", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=False, incoming_colour=player_colour, outgoing_colour =img.fark_colours[k], subfolder=f"num_by_colour\\{player_colour}\\")

    bust_filenames = os.listdir(img.output_dir+f"BASE\\bust\\")
    for file in bust_filenames:
        output_path = img.output_dir + f"num_by_colour\\{player_colour}\\"
        if "to_blank" in file:
            apply_colour_to_gif(img.output_dir + f"BASE\\bust\\" + file, "None", player_colour, output_path + file)
        else:
            apply_colour_to_gif(img.output_dir + f"BASE\\bust\\" + file, player_colour, "None", output_path + file)

    blank_frame = f"{os.getcwd()}\\dice_graphics\\BASE\\blank\\blank_frame.gif"
    for letter, f_colour in img.fark_colours.items():
        output_path = img.output_dir + f"num_by_colour\\{player_colour}\\"
        apply_colour_to_gif(blank_frame, f_colour, player_colour, output_path + f"blank_{letter}_to_blank.gif")
        apply_colour_to_gif(blank_frame, player_colour, f_colour, output_path + f"blank_to_blank_{letter}.gif")

## test start anim gifs

def do_window():
    import FreeSimpleGUI as sg

    chain_dir = img.output_dir + f"autogen\\full_roll\\"
    chain_gifs = os.listdir(chain_dir)
    chain = {}
    for i, char in enumerate(("f", "a", "r", "k", "l", "e")):
        advance = str(i+1)
        chain_gif = list(i for i in chain_gifs if i.startswith(f"farkle_chain_{char}_{advance}"))
        if chain_gif:
            chain[char] = chain_dir+chain_gif[0]

    sg.Text.char_width_in_pixels(("Courier New", 11))
    data_dict = {}
    letter_frames = {}
    images = list()
    longest_frames = 0
    for letter, filename in chain.items():
        with Image.open(filename) as f:
            n_frames = f.n_frames
        frames = n_frames
        if frames > longest_frames:
            longest_frames = frames
        accumImage = sg.tk.PhotoImage(file=filename, format=f'gif -index 0')
        data = [accumImage]
        for i in range(0, frames):
            deltaImage = sg.tk.PhotoImage(file=filename, format=f'gif -index {i}')
            accumImage.tk.call(accumImage, 'copy', deltaImage)
            data.append(accumImage.copy())
        data_dict[letter] = data
        letter_frames[letter] = frames
        images.append(sg.Image(key=letter))

    print(letter_frames)
    layout = [
        images,
        [sg.Button('Start/Stop')],
    ]
    window = sg.Window('Title', layout, finalize=True)
    index, running = 0, False
    changed = True
    #for letter in data_dict:
        #window[letter].update(data=data_dict[letter][0])

    print(f"Longest frames: {longest_frames}")
    while True:

        event, values = window.read(timeout=23)
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Start/Stop':
            running = not running

        if running:
            changed = True
            index = 0
        #elif event == sg.TIMEOUT_EVENT and running:
        if changed:
            changed = False
            index = index+1#letter_frames[letter]#longest_frames
            for letter, frames in letter_frames.items():
                #print(f"letter: {letter} / frames: {frames}")
                #index = (index+1) % frames#letter_frames[letter]#longest_frames
                if index > letter_frames[letter]:
                    do_index = 0
                    changed = False
                else:
                    do_index = index
                    changed = True
                #print(f"letter: {letter} / index: {index}")
                #window[letter].update_animation(chain[letter],  time_between_frames=20)
                window[letter].update(data=data_dict[letter][do_index])

    window.close()

def make_all_die_combinations():

    for die_val in ("1", "2", "3", "4", "5", "6"):
        transition_to_from([], "blank", die_val, start_roll=False, blank_before_incoming=False, end_roll=True,
                          output_name = f"blank_to_{die_val}", start_from_blank=True, end_with_blank=False, recolour=None,
                                continue_with_list=False, subfolder=f"BASE\\from_x_to_y")
        transition_to_from([], die_val, "blank", start_roll=True, blank_before_incoming=False, end_roll=False,
                          output_name = f"{die_val}_to_blank", start_from_blank=False, end_with_blank=True, recolour=None,
                                continue_with_list=False, subfolder=f"BASE\\from_x_to_y")

        transition_to_from([], die_val, die_val, start_roll=False, blank_before_incoming=False, end_roll=True, output_name = f"full_roll_{die_val}", start_from_blank=False, end_with_blank=False, recolour=None, continue_with_list=False, subfolder=f"BASE\\self_roll")
        for target_die in ("1", "2", "3", "4", "5", "6"):
            transition_to_from([], die_val, target_die, start_roll=False, blank_before_incoming=False, end_roll=True,
                        output_name = f"{die_val}_to_{target_die}", start_from_blank=False, end_with_blank=False, recolour=None, continue_with_list=False, subfolder=f"BASE\\from_x_to_y")


    for char in fark_dict:
        ### do a full roll. Not the blanks. Let me do the blank in combination with player colours instead. Just do the farkle colours.
        transition_to_from([], char, char, start_roll=False, blank_before_incoming=False, end_roll=True, output_name = f"full_roll_{char}", start_from_blank=False, end_with_blank=False, recolour =img.fark_colours[char], continue_with_list=False, subfolder=f"BASE\\self_roll")
        transition_to_from([], "blank", char, start_roll=False, blank_before_incoming=False, end_roll=False,
            output_name = f"blank_to_{char}", start_from_blank=False, end_with_blank=False, recolour =img.fark_colours[char],
                continue_with_list=False, outgoing_colour="None", subfolder="BASE\\farkle")
        transition_to_from([], char, "blank", start_roll=False, blank_before_incoming=False, end_roll=False,
            output_name = f"{char}_to_blank", incoming_colour="None", start_from_blank=False, end_with_blank=False, recolour =img.fark_colours[char],
                continue_with_list=False, subfolder="BASE\\farkle")

    for char in ("d", "b", "u", "s", "t"):
        ### do a full roll. Not the blanks. Let me do the blank in combination with player colours instead. Just do the bust colours.
        transition_to_from([], char, char, start_roll=False, blank_before_incoming=False, end_roll=True, output_name = f"full_roll_{char}", start_from_blank=False, end_with_blank=False, recolour =img.bust_colour, continue_with_list=False, subfolder=f"BASE\\self_roll")
        transition_to_from([], "blank", char, start_roll=False, blank_before_incoming=False, end_roll=False,
            output_name = f"blank_to_{char}", start_from_blank=False, end_with_blank=False, recolour =img.bust_colour,
                continue_with_list=False, outgoing_colour="None", subfolder="BASE\\bust")
        transition_to_from([], char, "blank", start_roll=False, blank_before_incoming=False, end_roll=False,
            output_name = f"{char}_to_blank", incoming_colour="None", start_from_blank=False, end_with_blank=False, recolour =img.bust_colour,
                continue_with_list=False, subfolder="BASE\\bust")

    # make grey frame-only for betweens
    blank_frame = []
    for filepath in sorted(img.frame_blanks):
        with Image.open(img.frame_dir + filepath) as f_blank:
            new = Image.new(mode="RGBA", size=f_blank.size)
            new.paste(f_blank)
            blank_frame.append(new)
    blank_frame[0].save(img.output_dir + "BASE\\blank\\blank_frame.gif", append_images=blank_frame[1:], save_all=True, duration=50, optimise=False, loop=0)


def held_and_used():
    """Makes a static image (for now)"""
    blank_frame = list(i for i in img.frame_blanks if i == "00.png")
    if blank_frame:
        blank_frame = blank_frame[0]

    button_held = "#F8DC5E"
    button_used = "#666354"
    with Image.open(img.frame_dir + blank_frame) as f_blank:
        frame_no = blank_frame.replace(".png", "")
        for val in "123456":
            char = list(i for i in img.chars_blanks if i == f"{val}.png")
            if char:
                char=char[0]

            with Image.open(img.chars_dir + char) as im:
                new = Image.new(mode="RGBA", size=f_blank.size)
                new.paste(f_blank)
                new.alpha_composite(im)
                print(f"char: {char}")

                new_image = recolour_frame(new, outgoing_colour=button_held, incoming_colour=button_held)
                new_image.save(f"{img.output_dir}BASE\\die_states\\{char.replace(".png", "")}_held.png")
                #new_image.show()
                new_image = recolour_frame(new, outgoing_colour=button_used, incoming_colour=button_used)
                new_image.save(f"{img.output_dir}BASE\\die_states\\{char.replace(".png", "")}_used.png")
                #new_image.show()


def make_single_frames(to_make="farklebustd", set_colour=None, output_dir=None):
    """For making a frame[0] version of each char. Currently I still only have them as blanks"""
    make_used = make_held = False
    if not output_dir:
        directory = f"{os.getcwd()}\\dice_graphics\\BASE\\stills\\"
    else:
        directory = output_dir
    print(f"Making single frames for `{to_make}`")
    if set_colour and set_colour == "used_die":
        make_used = True
        set_colour = img.button_used
    elif set_colour and set_colour == "held_die":
        make_held = True
        set_colour = img.button_held
    for char in to_make:
        if make_held:
            filename = directory+char+"_held.png"
        elif make_used:
            filename = directory+char+"_used.png"
        else:
            filename = directory+char+".png"
        if char in "123456":
            img.rotate_counter = int(char)
        get_roll(outgoing="blank", outgoing_colour=None, incoming=char, incoming_colour=set_colour, anim_frames=None, recolour=True, make_frame_zero=filename)


if "__main__" == __name__:

    import time
    start_time = time.time()

    make_single_frames()
    #colour_players_dice(player_colour="#78A73A", force_recolour=True)
    #held_and_used()
    end_time = time.time()
    seconds = (end_time - start_time)
    print("%.4f" % seconds) ## 2.4029 seconds as of 4.07pm, 2/5/26, for 82 files.

    #make_combination_image(make_farkle=False, make_bust=False, make_other="41b5162342", make_other_colour="#5E129C", other_subfolder="testing")#True)
    #make_player_dice("#11D49A")
    #do_window()
    #make_all_die_combinations()
    #compile_die()

