import time
import functools
import numpy as np
from PIL import Image


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


picname = "./zz.jpg"
text = extract_info(picname)
print("Extracted Information:", text)
print("The digital watermark is extracted successfully!")
