import sys
from PIL import Image
from math import *


def watermark_embed(filePath, watermarkInfo, outPath):
    img = Image.open(filePath)
    imgSize = img.size
    pixel = img.load()  # 获取图片所有的像素点
    len1 = floor((imgSize[0] * imgSize[1]) / (2 * (imgSize[0] + imgSize[1])))  # 数值的下舍整数
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

    new_array1 = []
    new_array2 = []
    x2 = ""
    for i in range(0, len(watermarkInfo)):
        new_array1.append(255 - ord(watermarkInfo[i]))  # ord()函数以字符(长度为1的字符串)作为参数，返回对应的ASCII或Unicode
    for i in range(0, len(x2)):
        new_array2.append(255 - ord(x2[i]))

    new_pixel1 = pixel[row, col]
    new_pixel2 = pixel[(new_pixel1[0] + new_pixel1[1]), (new_pixel1[2] + new_pixel1[0])]
    pix2 = int(new_pixel1[2])
    pix1 = int(new_pixel1[1])
    pix0 = int(new_pixel1[0])
    col = imgSize[1]
    row = imgSize[0]

    for i in range(0, len(watermarkInfo)):
        watermark_pix = new_array1.pop(0)
        pixel[(pix0 + pix1), (pix2 + pix1)] = (new_pixel2[0], watermark_pix, new_pixel2[2])
        pix2 = col - (new_pixel2[2] / 16)
        col = pix2
        pix1 = i
        pix0 = row - (new_pixel2[0] / 16)
        row = pix0
        if (new_pixel1[2] + i) < 0:
            print('Encryption intercepted')
            break
        if (new_pixel1[1] + i) < 0:
            print('Encryption intercepted')
            break
        new_pixel2 = pixel[(new_pixel1[0] + i + 1), (new_pixel1[2] + 1 + i)]
        pixel[imgSize[0] - 3, imgSize[1] - 3] = (0, len(watermarkInfo), len(x2))

    for i in range(0, len(x2)):
        watermark_pix = new_array2.pop(0)
        pixel[(new_pixel1[0] + new_pixel1[1]), (new_pixel1[2] + new_pixel1[1])] = (
            new_pixel2[0], watermark_pix, new_pixel2[2])
        pix2 = (col) - new_pixel2[2]
        col = pix2
        pix1 = i
        pix0 = (row) - new_pix1[0]
        row = pix0
        if (new_pixel1[2] + i) < 0:
            print('Encryption intercepted')
        if (new_pixel1[1] + i) < 0:
            print('Encryption intercepted')
        new_pix1 = pixel[(new_pixel1[0] + i), new_pixel1[2] + i]

    img.save(outPath)


if __name__ == '__main__':
    filePath = sys.argv[1]
    watermarkInfo = sys.argv[2]
    outPath = sys.argv[3]

    # filePath = "./input.png"
    # watermarkInfo = "1234567890@gmail.com-1234567890@gmail.com-49c567e3-8ded-4422-8524-84e9a1d86d35"
    # outPath = "./out.png"

    watermark_embed(filePath, watermarkInfo, outPath)

    print("The digital watermark is inserted successfully!")
