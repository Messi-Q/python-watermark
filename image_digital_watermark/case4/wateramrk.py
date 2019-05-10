import numpy as np
import cv2
import pywt
import random
import math
import cmath


def applyWatermarkDFT(imageMatrix, watermarkMatrix, alpha):
    shiftedDFT = np.fft.fftshift(np.fft.fft2(imageMatrix))
    watermarkedDFT = shiftedDFT + alpha * watermarkMatrix
    watermarkedImage = np.fft.ifft2(np.fft.ifftshift(watermarkedDFT))

    return watermarkedImage


def DFT(coverImage, watermarkImage):
    coverImage = cv2.resize(coverImage, (300, 300))
    cv2.imshow('Cover Image', coverImage)
    watermarkImage = cv2.resize(watermarkImage, (300, 300))
    cv2.imshow('Watermark Image', watermarkImage)

    watermarkedImage = applyWatermarkDFT(coverImage, watermarkImage, 10)
    watermarkedImage = np.uint8(watermarkedImage)
    cv2.imshow('Watermarked Image', watermarkedImage)


def DWT(coverImage, watermarkImage):
    coverImage = cv2.resize(coverImage, (300, 300))
    cv2.imshow('Cover Image', coverImage)
    watermarkImage = cv2.resize(watermarkImage, (150, 150))
    cv2.imshow('Watermark Image', watermarkImage)

    # DWT on cover image
    coverImage = np.float32(coverImage)
    coverImage /= 255;
    coeffC = pywt.dwt2(coverImage, 'haar')
    cA, (cH, cV, cD) = coeffC

    watermarkImage = np.float32(watermarkImage)
    watermarkImage /= 255;

    # Embedding
    coeffW = (0.4 * cA + 0.1 * watermarkImage, (cH, cV, cD))
    watermarkedImage = pywt.idwt2(coeffW, 'haar')
    cv2.imshow('Watermarked Image', watermarkedImage)

    # Extraction
    coeffWM = pywt.dwt2(watermarkedImage, 'haar')
    hA, (hH, hV, hD) = coeffWM

    extracted = (hA - 0.4 * cA) / 0.1
    extracted *= 255
    extracted = np.uint8(extracted)
    cv2.imshow('Extracted', extracted)


def DCT(coverImage, watermarkImage):
    coverImage = cv2.resize(coverImage, (512, 512))
    cv2.imshow('Cover Image', coverImage)
    watermarkImage = cv2.resize(watermarkImage, (64, 64))
    cv2.imshow('Watermark Image', watermarkImage)

    coverImage = np.float32(coverImage)
    watermarkImage = np.float32(watermarkImage)
    watermarkImage /= 255

    blockSize = 8
    c1 = np.size(coverImage, 0)
    c2 = np.size(coverImage, 1)
    max_message = (c1 * c2) / (blockSize * blockSize)

    w1 = np.size(watermarkImage, 0)
    w2 = np.size(watermarkImage, 1)

    watermarkImage = np.round(np.reshape(watermarkImage, (w1 * w2, 1)), 0)

    if w1 * w2 > max_message:
        print
        'Message too large to fit'

    message_pad = np.ones((max_message, 1), np.float32)
    message_pad[0:w1 * w2] = watermarkImage

    watermarkedImage = np.ones((c1, c2), np.float32)

    k = 50
    a = 0
    b = 0

    for kk in range(max_message):
        dct_block = cv2.dct(coverImage[b:b + blockSize, a:a + blockSize])
        if message_pad[kk] == 0:
            if dct_block[4, 1] < dct_block[3, 2]:
                temp = dct_block[3, 2]
                dct_block[3, 2] = dct_block[4, 1]
                dct_block[4, 1] = temp
        else:
            if dct_block[4, 1] >= dct_block[3, 2]:
                temp = dct_block[3, 2]
                dct_block[3, 2] = dct_block[4, 1]
                dct_block[4, 1] = temp

        if dct_block[4, 1] > dct_block[3, 2]:
            if dct_block[4, 1] - dct_block[3, 2] < k:
                dct_block[4, 1] = dct_block[4, 1] + k / 2
                dct_block[3, 2] = dct_block[3, 2] - k / 2
        else:
            if dct_block[3, 2] - dct_block[4, 1] < k:
                dct_block[3, 2] = dct_block[3, 2] + k / 2
                dct_block[4, 1] = dct_block[4, 1] - k / 2

        watermarkedImage[b:b + blockSize, a:a + blockSize] = cv2.idct(dct_block)
        if a + blockSize >= c1 - 1:
            a = 0
            b = b + blockSize
        else:
            a = a + blockSize

    watermarkedImage_8 = np.uint8(watermarkedImage)
    cv2.imshow('watermarked', watermarkedImage_8)


def SVD(coverImage, watermarkImage):
    cv2.imshow('Cover Image', coverImage)
    [m, n] = np.shape(coverImage)
    coverImage = np.double(coverImage)
    cv2.imshow('Watermark Image', watermarkImage)
    watermarkImage = np.double(watermarkImage)

    # SVD of cover image
    ucvr, wcvr, vtcvr = np.linalg.svd(coverImage, full_matrices=1, compute_uv=1)
    Wcvr = np.zeros((m, n), np.uint8)
    Wcvr[:m, :n] = np.diag(wcvr)
    Wcvr = np.double(Wcvr)
    [x, y] = np.shape(watermarkImage)

    # modifying diagonal component
    for i in range(0, x):
        for j in range(0, y):
            Wcvr[i, j] = (Wcvr[i, j] + 0.01 * watermarkImage[i, j]) / 255

    # SVD of wcvr
    u, w, v = np.linalg.svd(Wcvr, full_matrices=1, compute_uv=1)

    # Watermarked Image
    S = np.zeros((225, 225), np.uint8)
    S[:m, :n] = np.diag(w)
    S = np.double(S)
    wimg = np.matmul(ucvr, np.matmul(S, vtcvr))
    wimg = np.double(wimg)
    wimg *= 255
    watermarkedImage = np.zeros(wimg.shape, np.double)
    normalized = cv2.normalize(wimg, watermarkedImage, 1.0, 0.0, cv2.NORM_MINMAX)
    cv2.imshow('Watermarked Image', watermarkedImage)


def DWT_SVD(coverImage, watermarkImage):
    cv2.imshow('Cover Image', coverImage)
    [m, n] = np.shape(coverImage)
    coverImage = np.double(coverImage)
    cv2.imshow('Watermark Image', watermarkImage)
    watermarkImage = np.double(watermarkImage)

    # Applying DWT on cover image and getting four sub-bands
    coverImage = np.float32(coverImage)
    coverImage /= 255;
    coeffC = pywt.dwt2(coverImage, 'haar')
    cA, (cH, cV, cD) = coeffC

    # SVD on cA
    uA, wA, vA = np.linalg.svd(cA, full_matrices=1, compute_uv=1)
    [a1, a2] = np.shape(cA)
    WA = np.zeros((a1, a2), np.uint8)
    WA[:a1, :a2] = np.diag(wA)

    # SVD on cH
    uH, wH, vH = np.linalg.svd(cH, full_matrices=1, compute_uv=1)
    [h1, h2] = np.shape(cH)
    WH = np.zeros((h1, h2), np.uint8)
    WH[:h1, :h2] = np.diag(wH)

    # SVD on cV
    uV, wV, vV = np.linalg.svd(cV, full_matrices=1, compute_uv=1)
    [v1, v2] = np.shape(cV)
    WV = np.zeros((v1, v2), np.uint8)
    WV[:v1, :v2] = np.diag(wV)

    # SVD on cD
    uD, wD, vD = np.linalg.svd(cD, full_matrices=1, compute_uv=1)
    [d1, d2] = np.shape(cV)
    WD = np.zeros((d1, d2), np.uint8)
    WD[:d1, :d2] = np.diag(wD)

    # SVD on watermarked image
    uw, ww, vw = np.linalg.svd(watermarkImage, full_matrices=1, compute_uv=1)
    [x, y] = np.shape(watermarkImage)
    WW = np.zeros((x, y), np.uint8)
    WW[:x, :y] = np.diag(ww)

    # Embedding Process
    for i in range(0, x):
        for j in range(0, y):
            WA[i, j] = WA[i, j] + 0.01 * WW[i, j]

    for i in range(0, x):
        for j in range(0, y):
            WV[i, j] = WV[i, j] + 0.01 * WW[i, j]

    for i in range(0, x):
        for j in range(0, y):
            WH[i, j] = WH[i, j] + 0.01 * WW[i, j]

    for i in range(0, x):
        for j in range(0, y):
            WD[i, j] = WD[i, j] + 0.01 * WW[i, j]

    # Inverse of SVD
    cAnew = np.dot(uA, (np.dot(WA, vA)))
    cHnew = np.dot(uH, (np.dot(WH, vH)))
    cVnew = np.dot(uV, (np.dot(WV, vA)))
    cDnew = np.dot(uD, (np.dot(WD, vD)))

    coeff = cAnew, (cHnew, cVnew, cDnew)

    # Inverse DWT to get watermarked image
    watermarkedImage = pywt.idwt2(coeff, 'haar')
    cv2.imshow('Watermarked Image', watermarkedImage)


def DWT_DCT_SVD(coverImage, watermarkImage):
    coverImage = cv2.resize(coverImage, (512, 512))
    cv2.imshow('Cover Image', coverImage)
    watermarkImage = cv2.resize(watermarkImage, (256, 256))
    cv2.imshow('Watermark Image', watermarkImage)
    coverImage = np.float32(coverImage)

    coverImage /= 255
    coeff = pywt.dwt2(coverImage, 'haar')
    cA, (cH, cV, cD) = coeff

    watermarkImage = np.float32(watermarkImage)
    watermarkImage_dct = cv2.dct(watermarkImage)

    cA_dct = cv2.dct(cA)

    ua, sa, va = np.linalg.svd(cA_dct, full_matrices=1, compute_uv=1)
    uw, sw, vw = np.linalg.svd(watermarkImage, full_matrices=1, compute_uv=1)

    # Embedding
    alpha = 10
    sA = np.zeros((256, 256), np.uint8)
    sA[:256, :256] = np.diag(sa)
    sW = np.zeros((256, 256), np.uint8)
    sW[:256, :256] = np.diag(sW)
    W = sA + alpha * sW

    u1, w1, v1 = np.linalg.svd(W, full_matrices=1, compute_uv=1)
    ww = np.zeros((256, 256), np.uint8)
    ww[:256, :256] = np.diag(w1)
    Wmodi = np.matmul(ua, np.matmul(ww, va))

    widct = cv2.idct(Wmodi)
    watermarkedImage = pywt.idwt2((widct, (cH, cV, cD)), 'haar')
    cv2.imshow('watermarkedImage', watermarkedImage)


if __name__ == "__main__":
    coverImage = cv2.imread('brain.jpg', 0)
    watermarkImage = cv2.imread('lenna.jpg', 0)

    options = {1: DWT,
               2: DCT,
               3: DFT,
               4: SVD,
               5: DWT_SVD,
               6: DWT_DCT_SVD,
               }
    val = input('What type of embedding you want to perform?\n1.DWT\n2.DCT\n3.DFT\n4.SVD\n5.SVD-DWT\n6.SVD-DCT-DWT\n')
    options[val](coverImage, watermarkImage)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
