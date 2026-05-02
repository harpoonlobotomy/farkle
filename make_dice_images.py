""" I want to automate the actual dice animation making just a little. Right now I'm aligning the dice faces by hand and it's... a lot.

What I need is to have the dice face blanks, + the numbers, and to have it place and output the resulting images automatically. Which really shouldn't be all that hard, I think.

Around frame 4/5 I can do the switch between numbers. Only a few pixels of the incoming number are visible, I think it'd work.
So i need each number 'incoming' and 'outcoming', then I should be able to say '3 out, 5 in' and have 3 roll away to show 5. I think."""

"""
So, at the start of a run and/or when player colours are changed:
I need to generate the blank frames of incoming in the correct colours for each player die set. Save 'em in colour-identified folders so I don't regen each time. I need:
    blank > number
    number > blank # for rerolling
    blank > farkle
    blank > bust
^ reason for the blanks is largely so I avoid having to regenerate each number going to each of (farkle, bust) for each player for each colour. It might be better though. Not sure. Stick with this for now, especially as I've not actually got it properly animating in situ yet.

farkle>bust will never happen as it has to roll first. Same for the inverse as bust always leads to a new turn roll, not a start screen.
"""

from PIL import Image, ImageOps, ImageChops
import os

frame_path = f"{os.getcwd()}\\dice_graphics\\blanks\\frame_blanks\\"
frame_blanks = os.listdir(frame_path)
chars_path = f"{os.getcwd()}\\dice_graphics\\blanks\\chars_blanks\\"
chars_blanks = os.listdir(chars_path)

frame_mask_dir = f"{os.getcwd()}\\dice_graphics\\blanks\\face_masks\\"
frame_masks = os.listdir(frame_mask_dir)

standard_dice_colour = "#11D49A"
"""
open frame blank
make version of that frame blank with each Char blank on it. Save accordingly.
"""

output_dir = f"{os.getcwd()}\\dice_graphics\\autogen\\"

movement = {
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

fark_colours = { # for farkle_arcade
            "f": "#db270d",
            "a": "#ffb302",
            "r": "#71b335",
            "k": "#4e8f9a",
            "l": "#4e5b9a",
            "e": "#ae3aad"
        }


def get_roll(outgoing, incoming, anim_frames, recolour):

    if outgoing == "blank":
        outgoing_path = None
    else:
        print(f"outgoing: {outgoing}")
        outgoing_path = list(i for i in chars_blanks if i == f"{str(outgoing)}.png")[0]

    if incoming == "blank":
        incoming_path = None
    else:
        print(f"incoming: {incoming}")
        incoming_path = list(i for i in chars_blanks if i == f"{str(incoming)}.png")[0]

    if incoming and incoming in ("f", "a", "r", "k", "l", "e"):
        incoming_colour=fark_colours[incoming]
    elif incoming and incoming in ("dash", "b", "u", "s", "t"):
        incoming_colour="#330303"
    else:
        incoming_colour = standard_dice_colour # later this will be player colours

    if outgoing and outgoing in ("f", "a", "r", "k", "l", "e"):
        outgoing_colour=fark_colours[outgoing]
    elif outgoing and outgoing in ("dash", "b", "u", "s", "t"):
        outgoing_colour="#330303"
    else:
        outgoing_colour = standard_dice_colour

    outgoing_y_pos = None
    incoming_y_pos = None
    for filepath in sorted(frame_blanks):
        with Image.open(frame_path + filepath) as f_blank:
            #print(f"f_blank open: {filepath}")
            frame_no = filepath.replace(".png", "")

            new = Image.new(mode="RGBA", size=f_blank.size)
            new.paste(f_blank)
            if outgoing_path:
                with Image.open(chars_path + outgoing_path) as out_img:
                    if frame_no in movement["outgoing"]:
                        outgoing_y_pos = movement["outgoing"][frame_no]
                        new.alpha_composite(out_img, (0,outgoing_y_pos))

            if incoming_path:
                with Image.open(chars_path + incoming_path) as in_img:
                    if frame_no in movement["incoming"]:
                        incoming_y_pos = movement["incoming"][frame_no]
                        #print(f"incoming for frame no {frame_no}")
                        new.alpha_composite(in_img, (0,incoming_y_pos))

            if not outgoing_path and not incoming_path:
                print(f"NOT OUT OR IN: {frame_no}") # just means it's blank entirely. Not a problem. Don't know why I need this...

            if recolour:
                frame_mask = list(i for i in frame_masks if  i == filepath)
                if frame_mask:
                    frame_mask = frame_mask[0]
                else:
                    print(f"No frame mask found for {filepath}. All frame masks: \n{frame_masks}")

                new = recolour_frames(new, outgoing_colour, incoming_colour, frame_mask_dir + frame_mask, frame_no)
            anim_frames.append(new)
    return anim_frames


def recolour_frames(image:Image.Image, outgoing_colour="blue", incoming_colour="red", frame_mask=None, frame_no="06"):

    square = Image.new("RGBA", size=(100, 100), color=outgoing_colour)
    alt_square = Image.new("RGBA", size=(100, 100), color=incoming_colour)
    new_image = ImageChops.overlay(image, square)
    alt_image = ImageChops.overlay(image, alt_square)

    alt_image = alt_image.convert("RGB")
    new_image = new_image.convert("RGB")
    with Image.open(frame_mask) as mask:
        mask = mask.convert("1")
        new_image.paste(alt_image, mask=mask)

    return new_image

def transition_to_from(anim_frames, outgoing_char, incoming_char, start_roll=True, blank_before_incoming=True, end_roll=True, output_name=None, start_from_blank=False, end_with_blank=False, recolour=None, continue_with_list=False): # maybe set blank_before_incoming if char in FARKLE else false

    if not anim_frames:
        anim_frames = []

    if start_from_blank:
        anim_frames = get_roll(outgoing="blank", incoming=outgoing_char, anim_frames=anim_frames, recolour=recolour)

    if start_roll: # means we start with a full rotation of the outgoing, from 0
        anim_frames = get_roll(outgoing=outgoing_char, incoming=outgoing_char, anim_frames=anim_frames, recolour=recolour)

    if blank_before_incoming:
        anim_frames = get_roll(outgoing=outgoing_char, incoming="blank", anim_frames=anim_frames, recolour=recolour)
        anim_frames = get_roll(outgoing="blank", incoming=incoming_char, anim_frames=anim_frames, recolour=recolour)
    else:
        anim_frames = get_roll(outgoing=outgoing_char, incoming=incoming_char, anim_frames=anim_frames, recolour=recolour)

    if end_roll:
        anim_frames = get_roll(outgoing=incoming_char, incoming=incoming_char, anim_frames=anim_frames, recolour=recolour)

    if end_with_blank:
        anim_frames = get_roll(outgoing=incoming_char, incoming="blank", anim_frames=anim_frames, recolour=recolour)

    if not output_name:
        output_name = outgoing_char

    if continue_with_list:
        return anim_frames # for chaining longer strings.
    anim_frames[0].save(output_dir + f"full_roll\\{output_name}.gif", append_images=anim_frames[1:], save_all=True, duration=50, optimise=False, loop=0)
    return [] # <-- always returning anim_frames ruins the farkle intro rolls and potentially other things. Makes them jumpy and bad.

#transition_to_from(outgoing_char="3", incoming_char="f", start_roll=True, blank_before_incoming=True)

"""preroll anim: f:1, a:2 etc"""

fark_dict = {
    "f":"1",
    "a":"2",
    "r":"3",
    "k":"4",
    "l":"5",
    "e":"6",
}

#for k, v in fark_dict.items():
#    transition_to_from([], k, v, start_roll=True, blank_before_incoming=False, end_roll=False, output_name = f"{k}_to_{v}", start_from_blank=True, recolour="farkle", continue_with_list=False)

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
"""
rolls nicely:

if make_farkle_chain:
    anim_frames = []
    count = 0
    for k, char in fark_dict.items(): # through the whole lot
        if count:
            for _ in range(count):
                anim_frames = get_roll(outgoing="blank", incoming="blank", anim_frames=anim_frames, recolour="farkle")

        anim_frames = transition_to_from(anim_frames, "blank", k, start_roll=True, blank_before_incoming=False, end_roll=True, output_name = f"farkle_chain_{k}_{char}", start_from_blank=True, end_with_blank=False, recolour="farkle", continue_with_list=False)
        count += 1


"""
def make_combination_image(make_farkle = False, make_bust=False): ## redo this to use a dict instead of listing them all out like this.

    def make_from_list(incoming_list, output_path, colour=None):
        ## For full roll for each letter before changing, set end_roll=True.
        anim_frames = []
        for i, key in enumerate(incoming_list):
            if i == len(incoming_list)-3: # this one ends with blank so that even without the end_rolls on, it doesn't just jarringly end at the last letter but returns to blank.
                anim_frames = transition_to_from(anim_frames, outgoing_char=key, incoming_char=incoming_list[i+1], start_roll=False, blank_before_incoming=False, end_roll=False, output_name = output_path, start_from_blank=False, end_with_blank=True, recolour=colour, continue_with_list=False)
            elif i < len(incoming_list) -1:
                anim_frames = transition_to_from(anim_frames, outgoing_char=key, incoming_char=incoming_list[i+1], start_roll=False, blank_before_incoming=False, end_roll=False, output_name = output_path, start_from_blank=False, end_with_blank=False, recolour=colour, continue_with_list=True)

    farkle_list = ["blank", "f", "a", "r", "k", "l", "e", "blank"]
    bust_list = ["blank", "dash", "b", "u", "s", "t", "dash", "blank"]
    if make_farkle:
        make_from_list(farkle_list, output_path = "farkle_all_in_one", colour="farkle")
    if make_bust:
        make_from_list(bust_list, output_path = "bust_all_in_one", colour="bust")

make_combination_image(make_farkle=False, make_bust=False)#True)



## test start anim gifs

def do_window():
    import FreeSimpleGUI as sg

    chain_dir = output_dir + f"full_roll\\"
    chain_gifs = os.listdir(chain_dir)
    chain = {}
    for i, char in enumerate(("f", "a", "r", "k", "l", "e")):
        advance = str(i+1)
        chain_gif = list(i for i in chain_gifs if i.startswith(f"farkle_chain_{char}_{advance}"))
        if chain_gif:
            chain[char] = chain_dir+chain_gif[0]
    """    def chained():

        chained_output = []
        chain = {}
        chain_dir = output_dir + f"full_roll\\"
        chain_gifs = os.listdir(chain_dir)
        for i, char in enumerate(("f", "a", "r", "k", "l", "e")):
            advance = str(i+1)
            chain_gif = list(i for i in chain_gifs if i.startswith(f"farkle_chain_{char}_{advance}"))
            if chain_gif:
                chain_gif = chain_gif[0]
                chain[char] = chain_dir+chain_gif
                chained_output.append(sg.Image(source=chain_dir+chain_gif, key=char, background_color="blue"))
            else:
                print(f"No chain gif found for {i+1}, {char}")
        return chained_output, chain

    chain_images, chain_dict = chained()

    gif_layout = [chain_images]

    window = sg.Window(title="rolling dice intro", layout = gif_layout, finalize=True)

    f_image = Image.open(chain_dict["f"])
    frames = 33
    accumImage = sg.tk.PhotoImage(file=chain_dict["f"], format=f'gif -index 0')
    data = [accumImage]
    for i in range(1, frames):
        deltaImage = sg.tk.PhotoImage(file=chain_dict["f"], format=f'gif -index {i}')
        accumImage.tk.call(accumImage, 'copy', deltaImage)
        data.append(accumImage.copy())

    print(f"DATA: {data}")
    while True:
        event, values = window.read(10)
        for key in ("f"):
            for i in range(0,33): # single rotati
                window[key].update(data=data[i])#, duration=100)# time_between_frames=20)


import PySimpleGUI as sg"""
    """

THE FOLLOWING SETUP DOES WORK.

    """
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

do_window()
