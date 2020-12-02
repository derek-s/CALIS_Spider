# !/usr/bin/python 
# -*- coding: utf-8 -*-

# filePath: Do not edit
# Author: Derek.S(derekseli@outlook.com)
# Date: 2020-11-25 09:05:17
# LastEditors: Derek.S(derekseli@outlook.com)
# LastEditTime: 2020-12-02 17:47:19

from PIL import Image, ImageDraw
from io import BytesIO
import pytesseract

def downloadPassKeyImage(content):
    # download PassKey Image to disk
    with open("passkey.jpg", "wb") as PassKeyFile:
        PassKeyFile.write(content)
def processPassKey(content):
    # OCR PassKey
    downloadPassKeyImage(content)
    table = getBinTable()

    im = Image.open("passkey.jpg").convert('L').resize((300,100), Image.ANTIALIAS)
    binary = im.point(table, '1')
    binary.save("passkey_b.jpg")

    im = Image.open("passkey_b.jpg")

    # code = int(pytesseract.image_to_string(im, config=("-c tessedit"
    # "_char_whitelist=0123456789"
    # " -l eng"
    # " -psm 6"
    # " ")))
    # print(code)
    code = int(pytesseract.image_to_string(im, config=("-c tessedit"
    "_char_whitelist=0123456789"
    " -l opac"
    " -psm 6"
    " ")))
    print(code)
    return code

def getBinTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table
