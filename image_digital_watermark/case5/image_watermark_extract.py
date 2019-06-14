import sys
from PIL import Image
from math import *


def watermark_extract(filePath):
    img = Image.open(filePath)
    imgSize = img.size
    pix = img.load()
    len1 = floor((imgSize[0] * imgSize[1]) / (2 * (imgSize[0] + imgSize[1])))
    flag = 0
    if imgSize[0] > imgSize[1]:
        len2 = floor((imgSize[0] * imgSize[1]) / (len1 * (imgSize[0] - imgSize[1])))
        flag = 1
    elif imgSize[0] < imgSize[1]:
        len2 = floor((imgSize[0] * imgSize[1]) / (len1 * (imgSize[1] - imgSize[0])))
        flag = 2
    else:
        len2 = floor((imgSize[0] * imgSize[1]) / (len1 * (imgSize[0] + imgSize[1])))
    if flag == 0 or flag == 1:
        row = len1
        col = len2
    elif flag == 2:
        row = len2
        col = len1

    new_pix1 = pix[row, col]
    new_pix2 = pix[(new_pix1[0] + new_pix1[1]), (new_pix1[2] + new_pix1[0])]
    pix2 = int(new_pix1[2])
    pix1 = int(new_pix1[1])
    pix0 = int(new_pix1[0])
    col = imgSize[1]
    row = imgSize[0]
    var = pix[imgSize[0] - 3, imgSize[1] - 3]
    watermarkInfo_1 = ""
    watermarkInfo_2 = ""
    for i in range(0, int(var[1])):
        new_var = pix[(pix0 + pix1), (pix2 + pix1)]
        watermarkInfo_1 += (chr(255 - (new_var[1])))  # chr() ASCII -> 对应的字符
        pix2 = col - (new_pix2[2] / 16)
        col = pix2
        pix1 = i
        pix0 = row - (new_pix2[0] / 16)
        row = pix0
        new_pix2 = pix[(new_pix1[0] + i + 1), (new_pix1[2] + 1 + i)]

    for i in range(0, var[2]):
        new_var = pix[(pix0 + pix1), (pix2 + pix1)]
        watermarkInfo_2 += chr(255 - (new_var[2]))
        pix2 = col - new_pix2[2]
        col = pix2
        pix1 = i
        pix0 = row - new_pix2[0]
        row = pix0
        new_pix2 = pix[(new_pix1[0] + i + 1), (new_pix1[2] + 1 + i)]

    if var[2] != 0:
        watermarkInfo = watermarkInfo_2
        result = watermarkInfo.split("-", 2)
        print("资源所有者email：", result[0], "当前使用者email：", result[1], "资源ID：", result[2])
    else:
        watermarkInfo = watermarkInfo_1
        result = watermarkInfo.split("-", 2)
        print("资源所有者email：", result[0], "当前使用者email：", result[1], "资源ID：", result[2])


if __name__ == '__main__':
    outPath = sys.argv[1]
    # outPath = "./out.png"

    watermark_extract(outPath)
