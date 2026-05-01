"""make_coloured_dice.py"""

import base64
import os
from PIL import Image, ImageColor, ImageOps, ImageSequence

base_dir = f"{os.getcwd()}\\dice_graphics\\"
base_graphics = f"{base_dir}BASE\\"

"""farkle_dice = {
    "arcade":
        { # for farkle_arcade
            "die_1": ("black", "#db270d"),
            "die_2": ("black", "#ffb302"),
            "die_3": ("black", "#71b335"),
            "die_4": ("black", "#4e8f9a"),
            "die_5": ("black", "#4e5b9a"),
            "die_6": ("black", "#ae3aad")
        },
    "std":
        {
            "die_1": ("black", "#B44734"),
            "die_2": ("black", "#D6B72B"),
            "die_3": ("black", "#38B434"),
            "die_4": ("black", "#34A5B4"),
            "die_5": ("black", "#3476B4"),
            "die_6": ("black", "#7A34B4")
        }
}"""
farkle_dice = {
    "arcade":
        { # for farkle_arcade
            "f": "#db270d",
            "a": "#ffb302",
            "r": "#71b335",
            "k": "#4e8f9a",
            "l": "#4e5b9a",
            "e": "#ae3aad"
        },
    "std":
        {
            "f": "#B44734",
            "a": "#D6B72B",
            "r": "#38B434",
            "k": "#34A5B4",
            "l": "#3476B4",
            "e": "#7A34B4"
        }
}

def apply_colour(base_image, colour, target_path):

    """ Oh shit. I just realised this exists:
    multiply(image1: Image.Image, image2: Image.Image) -> Image.Image:
    in ImageChops. Instead of just colorising I can multiply, overlay, etc. This is what I needed. Good to know."""
    def modify_gif(im:Image.Image, colour, target_path):


        def for_each(im):
            im = im.convert("L")
            im = ImageOps.colorize(im, white=colour, black="black")

        #'im = im.convert("L")
        #new = ImageSequence.all_frames(im, ImageOps.colorize(im, white=colour, black="black"))
        new = []
        for frame_num in range(im.n_frames):
            try:
                im.seek(frame_num)
                new_frame = Image.new('RGBA', im.size)
                new_frame.paste(im)
                new_frame = new_frame.convert("L")
                new_frame = ImageOps.colorize(new_frame, white=colour, black="black")
                #new_frame = new_frame.convert(mode='P', palette=Image.ADAPTIVE, colors=color_depth)
                new.append(new_frame)
            except Exception as e:
                print(f"Failed to seek for {frame_num} from n_frames: {im.n_frames}")

        new[0].save(target_path, append_images=new[1:], save_all=True)

        with Image.open(target_path) as targ:
            print(f"TARGET PATH: {target_path}")
            print("targ.n_frames: ")
            print(targ.n_frames)
            #targ.show()
        return

    with Image.open(base_image) as im:
        if "gif" in base_image:
            modify_gif(im, colour, target_path)

        else:
            #im.show()
            im = im.convert("L")
            im = ImageOps.colorize(im, white=colour, black="black")
            #im.show()
            im.save(target_path)

def colour_player(player_no, player_colour):
    """Returns farkle[die_no] = output_path of recoloured images"""
    player = {}
    for subdir in ("still", "anim"):
        player[subdir] = {}
        base_die = os.listdir(base_graphics + f"{subdir}\\")
        for file in base_die:
            filepath = base_graphics + f"{subdir}\\" + file
            output_path = base_dir + f"{player_no}\\{subdir}\\{file}"
            die_no = file.replace(f"_{subdir}.png", "")
            apply_colour(filepath, player_colour, output_path)
            player[subdir][die_no] = output_path

    return player

def colour_farkle(farkle_colours):
    """Returns farkle[die_no] = output_path of recoloured images"""
    base_die = os.listdir(base_graphics + "farkle\\")
    farkle = {}
    for file in base_die:
        filepath = base_graphics + "farkle\\" + file
        output_path = base_dir + f"FARKLE\\STILL\\{file}"
        die_no = file.replace("_still.png", "")
        colour = farkle_colours[die_no]
        apply_colour(filepath, colour, output_path)
        farkle[die_no] = output_path
    return farkle


def recolour_dice(recolour_farkle=False, recolour_bust=False, recolour_player_1=False, recolour_player_2=False, game_theme=None):

    recolour_dict = {}
    if recolour_farkle:
        if game_theme and "arcade" in game_theme:
            farkle_colours = farkle_dice["arcade"]
        else:
            farkle_colours = farkle_dice["std"]
        recolour_dict["farkle"] = colour_farkle(farkle_colours)

    if recolour_player_1:
        recolour_dict["Player_1"] = colour_player("Player_1", recolour_player_1)
    if recolour_player_2:
        recolour_dict["Player_2"] = colour_player("Player_2", recolour_player_2)

    from make_base_64_from_image import auto_make_base64
    auto_make_base64()
    return recolour_dict

def make_directories():
    """Make graphic dirs and check if files are found"""
    incomplete_dirs = []
    for directory in ("BASE", "FARKLE", "BUST", "Player_1", "Player_2"):

        if not os.path.isdir(f"{os.getcwd()}\\dice_graphics\\{directory}\\"):
            os.makedirs(f"{os.getcwd()}\\dice_graphics\\{directory}\\")
        for inner_dir in ("anim", "still"):
            if not os.path.isdir(f"{os.getcwd()}\\dice_graphics\\{directory}\\{inner_dir}\\"):
                os.makedirs(f"{os.getcwd()}\\dice_graphics\\{directory}\\{inner_dir}\\")

        for root, dirs, files in os.walk(f"{os.getcwd()}\\dice_graphics\\{directory}\\"):
            if (files and len(files) < 6) or not files:
                #print(f"Files: {files}")
                #rint(f"Files are missing from {root}")
                incomplete_dirs.append(root)
    print(f"Incomplete dirs: {incomplete_dirs}")
    return incomplete_dirs



if __name__ == "__main__":
    #incomplete_dirs = make_directories()
    #if incomplete_dirs:
    recolour_dice(recolour_player_1="aqua")

    """import FreeSimpleGUI as sg
    b_str = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAIAAAD/gAIDAAABp0lEQVR4nO3dzUrDQBRA4alOEbRFXOYFXPn+D+MLZC3+gFTBxcUytlI80oSZzPlWpYvQHm7SaQjM6uFuk77d396knzbrnHrysvs4eOfx6XX/+mL2z9OwXM5UzNF2fZl6tS2++/Puc18m5svJArIz9Zcpi0pOFr9m9XydOi3KxK+kkwUYCzAWkHtbo/9PVHKyAGMBxgKMBRgLMBZgLGCmRdb49j7RkYfrq7SkyRonKzX1wQ94GgLGAowFGAswFmCsnmINM66zciff8yyan6w5GQswFmAswFiAsQBjAcYCjAUYq5G/OyO5I1zDf6NmJmuc8V5787FqYCzAWICxAGMBxlpirKGCdZb34Jc4WTUwFmAswFiAsQBjAcYCjAUYCzAWYCzAWICxAGMBxgKMBRgLMBZgLMBYgLEAYwHGAowFGAswFmAswFiAsQBjAcYCjAUYCzAWYCzAWJXFGn570LiGp48rfVp5aDDNMU9DwFiAsQBjATl2Z3APi9PcwwLzNASMxRelsS+WV65jUSY4WUCO/dXKnQ2dr3Km4nfQXeiwlTtnltw5M53LF/YvPwIqvRiRAAAAAElFTkSuQmCC'
    #b_str = eval(b_str)
    #b_str = base64.decodebytes(b_str)

    layout = [[
        sg.Column(layout=[[sg.Image(data=b_str)]])
    ]]

    window = sg.Window(layout=layout, title="window")
    window.read(100)
    import time
    time.sleep(5)
    #base64.decode(b_str, )"""


