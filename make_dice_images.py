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

"""
open frame blank
make version of that frame blank with each Char blank on it. Save accordingly.
"""

output_dir = f"{os.getcwd()}\\dice_graphics\\autogen\\"

movement = {
    "outgoing": { ## how many pixels down on 7 from 0 (final y position, not additive per frame.)
            0:0,
            1:6,
            2:14,
            3:24,
            4:40,
            5:52,
            6:63,
            },
    "incoming":
        {
            4: -75,
            5: -64,
            6: -53,
            7: -38,
            8: -28,
            9: -16,
            10: -6,
        }
}

"""
test: 3 > "F" > 5
"""

for filepath in frame_blanks:
    with Image.open(frame_path + filepath) as f_blank:
        for section in ("incoming", "outgoing"):
            for frame_no, y_pos in movement[section].items():
                if filepath == f"{str(frame_no)}.png":
                    for char_path in chars_blanks:
                        new = Image.new(mode="RGBA", size=f_blank.size)
                        new.paste(f_blank)
                        with Image.open(chars_path + char_path) as char:
                            print(f"Char.mode: {char.mode}")
                            new.alpha_composite(char, (0,y_pos))
                            new_name = "char_" + char_path.replace(".png", "_") + "frame_" + filepath
                            output_path = output_dir + section + "\\" + new_name
                            new.save(output_path)
