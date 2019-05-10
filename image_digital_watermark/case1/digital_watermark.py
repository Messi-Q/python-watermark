from PIL import Image
import time
import numpy as np
import functools
import sys


def embedding_info(picname, savename, text):
    text += '#%#'  # As end flag
    try:
        im = np.array(Image.open(picname))
    except:
        print("Cannot obtain image, please check file name")
        time.sleep(3)
        sys.exit()

    rows, columns, colors = im.shape
    embed = []
    for c in text:
        bin_sign = (bin(ord(c))[2:]).zfill(16)
        for i in range(16):
            embed.append(int(bin_sign[i]))

    count = 0
    for row in range(rows):
        for col in range(columns):
            for color in range(colors):
                if count < len(embed):
                    im[row][col][color] = im[row][col][color] // 2 * 2 + embed[count]
                    count += 1

    Image.fromarray(im).save(savename)


def extract_info(picname):
    try:
        im = np.array(Image.open(picname))
    except:
        print("Cannot obtain image, please check file name")
        time.sleep(2)
        sys.exit()

    rows, columns, colors = im.shape
    text = ""
    extract = np.array([], dtype=int)

    count = 0
    for row in range(rows):
        for col in range(columns):
            for color in range(colors):
                extract = np.append(extract, im[row][col][color] % 2)
                count += 1
                if count % 16 == 0:
                    bcode = functools.reduce(lambda x, y: str(x) + str(y), extract)
                    cur_char = chr(int(bcode, 2))
                    text += cur_char
                    if cur_char == '#' and text[-3:] == '#%#':
                        return text[:-3]
                    extract = np.array([], dtype=int)


def check_user():
    user_pass = {}
    username = input("Initial capital letter:")
    password = input("your birthday:")
    if username not in user_pass or user_pass[username] != password:
        print("email to author")
        time.sleep(2)
        sys.exit()


def check_pic_format(picture):
    if picture[-4:] != '.png':
        print("Not png, repeat")
        time.sleep(2)
        sys.exit()


def main():
    # check_user()
    print("Welcome to Digital Watermarking Tool")
    choose = input("options:1.Watermark Embedding 2.Watermark Extracting\n")
    if choose == '1':
        picname = input("Select an image to embed: ")
        check_pic_format(picname)
        text = input("Embedded Information: ")
        savename = 'resourceEmbedded.png'
        embedding_info(picname, savename, text)
        print("The digital watermark is inserted successfully!")
    elif choose == '2':
        picname = input("select an image to extract: ")
        check_pic_format(picname)
        text = extract_info(picname)
        print("Extracted Information:", text)
        print("The digital watermark is extracted successfully!")
    else:
        print("error")
        time.sleep(2)
        sys.exit()


if __name__ == '__main__':
    main()
