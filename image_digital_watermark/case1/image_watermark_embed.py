from PIL import Image
import time
import numpy as np
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


picname = "./zfb.jpg"
pic_suffix = picname.split(".", 2)[2]
print(pic_suffix)
text = "qian"
savename = './zz' + "." + pic_suffix
embedding_info(picname, savename, text)
print("The digital watermark is inserted successfully!")
