from PIL import Image
from math import *


def watermark_embed():
    im1 = Image.open("input.png")
    im2 = im1.size
    pix = im1.load()
    abc = floor((im2[0] * im2[1]) / (2 * (im2[0] + im2[1])))
    flag = 0
    if (im2[0] > im2[1]):
        efg = floor((im2[0] * im2[1]) / (abc * (im2[0] - im2[1])))
        flag = 1
    elif (im2[0] < im2[1]):
        efg = floor((im2[0] * im2[1]) / (abc * (im2[1] - im2[0])))
        flag = 2
    else:
        efg = floor((im2[0] * im2[1]) / (abc * (im2[0] + im2[1])))
    if (flag == 0 or flag == 1):
        ro = abc
        co = efg
    elif (flag == 2):
        ro = efg
        co = abc

    new_arr1 = []
    new_arr2 = []
    x1 = input("Enter the 1st string:")
    x2 = ""
    for i in range(0, len(x1)):
        new_arr1.append(255 - ord(x1[i]))
    for i in range(0, len(x2)):
        new_arr2.append(255 - ord(x2[i]))
    new_pix = pix[ro, co]
    new_pix1 = pix[(new_pix[0] + new_pix[1]), (new_pix[2] + new_pix[0])]
    qwer = int(new_pix[2])
    jkl = int(new_pix[1])
    fgh = int(new_pix[0])
    co = im2[1]
    ro = im2[0]

    for i in range(0, len(x1)):
        ele = new_arr1.pop(0)
        pix[(fgh + jkl), (qwer + jkl)] = (new_pix1[0], ele, new_pix1[2])
        qwer = co - (new_pix1[2] / 4)
        co = qwer
        jkl = i
        fgh = ro - (new_pix1[0] / 4)
        ro = fgh
        if ((new_pix[2] + i) < 0):
            print('Encryption intercepted')
            break
        if ((new_pix[1] + i) < 0):
            print('Encryption intercepted')
            break
        new_pix1 = pix[(new_pix[0] + i + 1), (new_pix[2] + 1 + i)]
    pix[im2[0] - 3, im2[1] - 3] = (0, len(x1), len(x2))

    for i in range(0, len(x2)):
        ele = new_arr2.pop(0)
        pix[(new_pix[0] + new_pix[1]), (new_pix[2] + new_pix[1])] = (new_pix1[0], ele, new_pix1[2])
        qwer = (co) - new_pix1[2]
        co = qwer
        jkl = i
        fgh = (ro) - new_pix1[0]
        ro = fgh
        if ((new_pix[2] + i) < 0):
            print('Encryption intercepted')
        if ((new_pix[1] + i) < 0):
            print('Encryption intercepted')
        new_pix1 = pix[(new_pix[0] + i), new_pix[2] + i]
    im1.save("1.bmp")


def watermark_extract():
    im1 = Image.open("1.bmp")
    im2 = im1.size
    pix = im1.load()
    abc = floor((im2[0] * im2[1]) / (2 * (im2[0] + im2[1])))
    flag = 0
    if (im2[0] > im2[1]):
        efg = floor((im2[0] * im2[1]) / (abc * (im2[0] - im2[1])))
        flag = 1
    elif (im2[0] < im2[1]):
        efg = floor((im2[0] * im2[1]) / (abc * (im2[1] - im2[0])))
        flag = 2
    else:
        efg = floor((im2[0] * im2[1]) / (abc * (im2[0] + im2[1])))
    if (flag == 0 or flag == 1):
        ro = abc
        co = efg
    elif (flag == 2):
        ro = efg
        co = abc
    new_pix = pix[ro, co]
    new_pix1 = pix[(new_pix[0] + new_pix[1]), (new_pix[2] + new_pix[0])]
    qwer = int(new_pix[2])
    jkl = int(new_pix[1])
    fgh = int(new_pix[0])
    co = im2[1]
    ro = im2[0]
    var = pix[im2[0] - 3, im2[1] - 3]
    bv = ''
    bv1 = ''
    for i in range(0, int(var[1])):
        new_var = pix[(fgh + jkl), (qwer + jkl)]
        arre = (chr(255 - (new_var[1])))
        bv = bv + arre
        qwer = co - (new_pix1[2] / 4)
        co = qwer
        jkl = i
        fgh = ro - (new_pix1[0] / 4)
        ro = fgh
        new_pix1 = pix[(new_pix[0] + i + 1), (new_pix[2] + 1 + i)]
    for i in range(0, var[2]):
        new_var = pix[(fgh + jkl), (qwer + jkl)]
        arr1 = chr(255 - (new_var[2]))
        bv1 += arr1
        qwer = co - new_pix1[2]
        co = qwer
        jkl = i
        fgh = ro - new_pix1[0]
        ro = fgh
        new_pix1 = pix[(new_pix[0] + i + 1), (new_pix[2] + 1 + i)]
    print('string-1 is', bv)
    if (var[2] != 0):
        print('string-2 is', bv1)


watermark_embed()
print("============================")
watermark_extract()
