import cv2 as cv
import numpy
import hashlib
import sys

ColRange = 16
RowRange = 16


def hash(ID):
    hash_method = hashlib.sha256()
    hash_method.update(ID.encode('utf-8'))
    binary = []
    temp = []
    result = []
    str = hash_method.hexdigest()

    for i in str:
        if i >= '0' and i <= '9':
            b = ord(i) - 48
        else:
            b = ord(i) - 55
        while (len(temp) < 4):
            temp.append(b % 2)
            b //= 2
        while (len(temp) > 0):
            binary.append(temp.pop())

    result.append(str)
    result.append(binary)
    return result


def arnold(picture):
    An = numpy.zeros([height, width, 3])
    n = 2
    a = 3
    b = 5
    N = min(height, width)
    for i in range(1, 2):
        for y in range(N):
            for x in range(N):
                xx = (x + b * y) % N
                yy = (a * x + (a * b + 1) * y) % N
                An[yy][xx] = picture[y][x]
    if height > width:
        for y in range(N, height):
            for x in range(N):
                An[y][x] = picture[y][x]
    elif height < width:
        for y in range(N):
            for x in range(N, width):
                An[y][x] = picture[y][x]

    return An


def sha_extract(picture):
    s = ''
    count = 1
    num = 0
    for i in range(RowRange):
        for j in range(ColRange):
            if count == 4:
                count = 1
                num = num * 2 + picture[i, j][1] % 2
                if num <= 9:
                    s = s + chr(int(num + 48))
                else:

                    s = s + chr(int(num + 87))
                num = 0
            else:
                num = num * 2 + picture[i, j][1] % 2
                count += 1
    return s


filePath = sys.argv[1]
ID = sys.argv[2]

sha, info = hash(ID)
img = cv.imread(filePath)
height = img.shape[0]
width = img.shape[1]

if sha == sha_extract(arnold(img)):
    print(sha)
    print(sha_extract(arnold(img)))
    print("Copyright verified successfully")
else:
    print(sha)
    print(sha_extract(arnold(img)))
    print("Copyright verified unsuccessfully")

