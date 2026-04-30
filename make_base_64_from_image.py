def make_base_64(png_file = r"D:\Git_Repos\farkle\dice_graphics\still\1_still_100px.png", print=False, return_b=False, return_str=True):

    import base64
    with open(png_file, "rb") as f:
        encoded_image = base64.b64encode(f.read())
        #decoded_image = encoded_image.decode('utf8').replace("'", '"')
    if print:
        print(f"encoded image: {encoded_image}")
        #print(f"decoded image: {decoded_image}")
    if return_b:
        return encoded_image
    if return_str:
        return str(encoded_image)


def auto_make_base64():

    replace_in_json = False

    import os, json
    base_64_file = r"D:\Git_Repos\farkle\dice_graphics\die_base64.json"
    with open(base_64_file, "r") as base_64:
        dictionary = json.load(base_64)

    base_dir = os.getcwd() + "\\" + "dice_graphics\\"
    input_folders = os.listdir(base_dir)#[r"D:\Git_Repos\farkle\dice_graphics\BASE\anim", r"D:\Git_Repos\farkle\dice_graphics\BASE\still"]

    for directory in input_folders:
        for root, dirs, files in os.walk(base_dir + directory):
            if "BASE" in root:
                continue
            if files:
                print(f"Files: {files}")
                for file in files:
                    if dictionary.get(file.replace("_100px", "")) and not replace_in_json:
                        continue
                    else:
                        base_64_str = make_base_64(png_file = root + "\\" + file, return_str=True)
                        name = file.replace("_100px", "")
                        dictionary[name] = str(base_64_str)

        """for graphic in os.listdir(base_dir + directory):
        print(f"dirs: {tuple(dirs)}")
            print(f"GRAPHIC: {graphic}")
            """

    with open(base_64_file, "w") as base_64:
        json.dump(dictionary, base_64, indent=2)

if __name__ == "__main__":

    #make_base_64()
    auto_make_base64()
