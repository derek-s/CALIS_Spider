# !/usr/bin/python 
# -*- coding: utf-8 -*-

# filePath: Do not edit
# Author: Derek.S(derekseli@outlook.com)
# Date: 2020-12-02 12:35:37
# LastEditors: Derek.S(derekseli@outlook.com)
# LastEditTime: 2020-12-02 13:54:05

import requests
import time
import random
from PIL import Image, ImageDraw
import sys
from io import BytesIO

sys.path.append("..")
from ua import UAMaker


def downloadPassKeyImage(content, filename):
    # download PassKey Image to disk
    with open(filename, "wb") as PassKeyFile:
        PassKeyFile.write(content)

def getBinTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

if __name__ == "__main__":
    # im = Image.open("passkey.jpg").convert('L').resize((300,100), Image.ANTIALIAS)
    # imGray = im.convert('L')
    # table = getBinTable()
    # binary = imGray.point(table, '1')
    # binary.save("passkey_b.jpg")

    x = 500
    t = 201
    passKeyUrl = "http://opac.calis.edu.cn/opac/security"
    

    while(t <= x):
        uaString = UAMaker().random_PC()
        headers = {
            "user-agent": uaString
        }
        r = requests.get(passKeyUrl)
        filename = str(t) + ".jpg"
        downloadPassKeyImage(r.content, filename)
        im = Image.open(filename).convert('L').resize((300,100), Image.ANTIALIAS)
        imGray = im.convert('L')
        table = getBinTable()
        binary = imGray.point(table, '1')
        binary.save(str(t) + "_b.jpg")
        t = t + 1
        time.sleep(random.randint(3, 15))