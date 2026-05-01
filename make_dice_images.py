""" I want to automate the actual dice animation making just a little. Right now I'm aligning the dice faces by hand and it's... a lot.

What I need is to have the dice face blanks, + the numbers, and to have it place and output the resulting images automatically. Which really shouldn't be all that hard, I think.

Around frame 4/5 I can do the switch between numbers. Only a few pixels of the incoming number are visible, I think it'd work.
So i need each number 'incoming' and 'outcoming', then I should be able to say '3 out, 5 in' and have 3 roll away to show 5. I think."""

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

def get_strength(in_or_out, y_pos):
    """
    colour strength: [[v v roughly]]
        "incoming":
            strength percent ==  (incoming[frame_no] + 100)

        "outgoing":
            strength percent == (100 - (outgoing[frame_no] * 2))

    """
    if in_or_out == "incoming":
        strength = y_pos + 100
    else:
        strength = 100 - (y_pos*2)
        if strength < 0:
            strength = 0
    print(f"Strength for {in_or_out} // y_pos: {y_pos}:  ``{strength}``\n")
    return strength


fark_colours = { # for farkle_arcade
            "f": "#db270d",
            "a": "#ffb302",
            "r": "#71b335",
            "k": "#4e8f9a",
            "l": "#4e5b9a",
            "e": "#ae3aad"
        }
"""
test: 3 > "F" > 5
"""

"""for filepath in frame_blanks:
    with Image.open(frame_path + filepath) as f_blank:
        for section in ("incoming", "outgoing"):
            for frame_no, y_pos in movement[section].items():
                if filepath == f"{frame_no}.png":
                    for char_path in chars_blanks:
                        new = Image.new(mode="RGBA", size=f_blank.size)
                        new.paste(f_blank)
                        with Image.open(chars_path + char_path) as char:
                            print(f"Char.mode: {char.mode}")
                            new.alpha_composite(char, (0,y_pos))
                            new_name = "char_" + char_path.replace(".png", "_") + "frame_" + filepath
                            output_path = output_dir + section + "\\" + new_name
                            new.save(output_path)"""

def get_roll(outgoing, incoming, anim_frames, recolour):

    if outgoing == "blank":
        outgoing_path = None
    else:
        print(f"incoming: {incoming}")
        outgoing_path = list(i for i in chars_blanks if i == f"{str(outgoing)}.png")[0]

    if incoming == "blank":
        incoming_path = None
    else:
        print(f"incoming: {incoming}")
        incoming_path = list(i for i in chars_blanks if i == f"{str(incoming)}.png")[0]

    if incoming and incoming in ("f", "a", "r", "k", "l", "e"):
        incoming_colour=fark_colours[incoming]
    else:
        incoming_colour = standard_dice_colour # later this will be player colours

    if outgoing and outgoing in ("f", "a", "r", "k", "l", "e"):
        outgoing_colour=fark_colours[outgoing]
    else:
        outgoing_colour = standard_dice_colour

    outgoing_y_pos = None
    incoming_y_pos = None
    for filepath in sorted(frame_blanks):
        with Image.open(frame_path + filepath) as f_blank:
            print(f"f_blank open: {filepath}")
            frame_no = filepath.replace(".png", "")

            new = Image.new(mode="RGBA", size=f_blank.size)
            new.paste(f_blank)
            if outgoing_path:
                with Image.open(chars_path + outgoing_path) as out_img:
                    if frame_no in movement["outgoing"]:
                        outgoing_y_pos = movement["outgoing"][frame_no]
                        print(f"outgoing for frame no {frame_no}")
                        new.alpha_composite(out_img, (0,outgoing_y_pos))
                        print("outgoing_y_pos")
                        #if recolour:
                            #new = recolour_frames(new, incoming_colour, outgoing_colour, y_pos, get_strength("outgoing", y_pos))


            if incoming_path:
                with Image.open(chars_path + incoming_path) as in_img:
                    if frame_no in movement["incoming"]:
                        incoming_y_pos = movement["incoming"][frame_no]
                        print(f"incoming for frame no {frame_no}")
                        new.alpha_composite(in_img, (0,incoming_y_pos))

            if not outgoing_path and not incoming_path:
                print(f"NOT OUT OR IN: {frame_no}")
                #new_name = "char_" + char_path.replace(".png", "_") + "frame_" + filepath
                #output_path = output_dir + "full_roll\\" + new_name
            print(f"FRAME: {frame_no}")
            if recolour:
                frame_mask = list(i for i in frame_masks if  i == filepath)
                if frame_mask:
                    frame_mask = frame_mask[0]
                else:
                    print(f"No frame mask found for {filepath}. All frame masks: \n{frame_masks}")
                """if incoming_y_pos:
                    print(f"incoming_y_pos: {incoming_y_pos}")
                    incoming_strength = get_strength("incoming", incoming_y_pos)
                else:
                    incoming_strength = 0
                if outgoing_y_pos:
                    print(f"outgoing_y_pos: {outgoing_y_pos}")
                    outgoing_strength = get_strength("outgoing", outgoing_y_pos)
                else:
                    outgoing_strength = 0
                if not incoming_strength and not outgoing_strength:
                    incoming_strength = 100
                print(f"incominmg strength = {incoming_strength}\noutgoing_strength: {outgoing_strength}\n")
                total = 100/(incoming_strength + outgoing_strength)
                incoming_strength = incoming_strength * total
                outgoing_strength = outgoing_strength * total
                print(f"incominmg strength = {incoming_strength}\noutgoing_strength: {outgoing_strength}\n")

                print(f"incoming colour: {incoming_colour}")"""
                new = recolour_frames(new, outgoing_colour, incoming_colour, frame_mask_dir + frame_mask, frame_no)
            anim_frames.append(new)
                #new.save(output_path)
    return anim_frames

def recolour_frames(image:Image.Image, outgoing_colour="blue", incoming_colour="red", frame_mask=None, frame_no="06"):

    #square = Image.new("RGBA", size=(100, pos_y+100), color=colour)
    square = Image.new("RGBA", size=(100, 100), color=outgoing_colour)
    alt_square = Image.new("RGBA", size=(100, 100), color=incoming_colour)
    new_image = ImageChops.overlay(image, square)
    alt_image = ImageChops.overlay(image, alt_square)

    #new_image = ImageChops.blend(new_image, alt_image, int(frame_mask/100))
    alt_image = alt_image.convert("RGB")
    new_image = new_image.convert("RGB")
    with Image.open(frame_mask) as mask:
        mask = mask.convert("1")
        new_image.paste(alt_image, mask=mask)

    #im = ImageOps.colorize(im, white=colour, black="black")
    #if pos_y:
        #image.paste(new_image, (0, 0))
        #image.show()
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

        """for filepath in sorted(frame_blanks):
            with Image.open(frame_path + filepath) as f_blank:
                frame_no = filepath.replace(".png", "")
                char_path = list(i for i in chars_blanks if i == f"{str(outgoing_char)}.png")[0]
                new = Image.new(mode="RGBA", size=f_blank.size)
                new.paste(f_blank)
                with Image.open(chars_path + char_path) as char:
                    if movement["outgoing"].get(frame_no):
                        y_pos = movement["outgoing"][frame_no]
                        new.alpha_composite(char, (0,y_pos))
                    if movement["incoming"].get(frame_no):
                        y_pos = movement["incoming"][frame_no]
                        new.alpha_composite(char, (0,y_pos))

                    new_name = "char_" + char_path.replace(".png", "_") + "frame_" + filepath
                    output_path = output_dir + "full_roll\\" + new_name
                    anim_frames.append(new)
                    new.save(output_path)"""

    if continue_with_list:
        return anim_frames # for chaining longer strings.
    print(f"len anim frames for {incoming_char}: {len(anim_frames)}")
    anim_frames[0].save(output_dir + f"full_roll\\{output_name}.gif", append_images=anim_frames[1:], save_all=True, duration=50)
    return []

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
#    transition_to_from(k, v, start_roll=True, blank_before_incoming=False, end_roll=False, output_name = f"{k}_to_{v}", start_from_blank=True, recolour="farkle", continue_with_list=False)

make_farkle_chain = False#True

if make_farkle_chain:
    anim_frames = []
    count = 0
    for k, char in fark_dict.items(): # through the whole lot
        if count:
            for _ in range(count):
                anim_frames = get_roll(outgoing="blank", incoming="blank", anim_frames=anim_frames, recolour="farkle")

        anim_frames = transition_to_from(anim_frames, "blank", k, start_roll=False, blank_before_incoming=False, end_roll=True, output_name = f"farkle_chain_{k}_{char}", start_from_blank=True, end_with_blank=True, recolour="farkle", continue_with_list=False)
        count += 1

make_farkle_in_one = False#True
if make_farkle_in_one:
    anim_frames = []
    anim_frames = transition_to_from(anim_frames, "blank", "f", start_roll=True, blank_before_incoming=False, end_roll=False, output_name = f"farkle_in_one", start_from_blank=True, end_with_blank=False, recolour="farkle", continue_with_list=True)
    anim_frames = transition_to_from(anim_frames, "f", "a", start_roll=False, blank_before_incoming=False, end_roll=False, output_name = f"farkle_in_one", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=True)
    anim_frames = transition_to_from(anim_frames, "a", "r", start_roll=False, blank_before_incoming=False, end_roll=False, output_name = f"farkle_in_one", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=True)
    anim_frames = transition_to_from(anim_frames, "r", "k", start_roll=False, blank_before_incoming=False, end_roll=False, output_name = f"farkle_in_one", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=True)
    anim_frames = transition_to_from(anim_frames, "k", "l", start_roll=False, blank_before_incoming=False, end_roll=False, output_name = f"farkle_in_one", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=True)
    anim_frames = transition_to_from(anim_frames, "l", "e", start_roll=False, blank_before_incoming=False, end_roll=False, output_name = f"farkle_in_one", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=True)
    anim_frames = transition_to_from(anim_frames, "e", "blank", start_roll=False, blank_before_incoming=False, end_roll=True, output_name = f"farkle_in_one", start_from_blank=False, end_with_blank=False, recolour="farkle", continue_with_list=False)



## test start anim gifs

def do_window():
    import FreeSimpleGUI as sg

    chain_dir = output_dir + f"full_roll\\"
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
    filename = chain_dir+f"farkle_chain_f_1.gif"
    frames = 44
    accumImage = sg.tk.PhotoImage(file=filename, format=f'gif -index 0')
    print(dir(accumImage))
    data = [accumImage]
    for i in range(1, frames):
        print(f"i: {i}")
        deltaImage = sg.tk.PhotoImage(file=filename, format=f'gif -index {i}')
        accumImage.tk.call(accumImage, 'copy', deltaImage)
        data.append(accumImage.copy())

    layout = [
        [sg.Image(key='-IMAGE-')],
        [sg.Button('Start/Stop')],
    ]
    window = sg.Window('Title', layout, finalize=True)
    index, running = 0, False
    window['-IMAGE-'].update(data=data[0])

    while True:

        event, values = window.read(timeout=50)
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Start/Stop':
            running = not running
        elif event == sg.TIMEOUT_EVENT and running:
            index = (index+1) % frames
            window['-IMAGE-'].update(data=data[index])

    window.close()

do_window()
