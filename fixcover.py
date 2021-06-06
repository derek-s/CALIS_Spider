#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: fixcover.py
# DATE: 2021/06/04
# TIME: 13:42:43

# DESCRIPTION: fix cover

import time
import random

import requests

from db import collection
from bs4 import BeautifulSoup as bas
from ua import UAMaker



def dban(isbn):
    url = "" + isbn.replace("-", "")

    uaString = UAMaker().random_PC()

    headers = {
        "user-agent": uaString
    }
    
    s = requests.session()

    datailPage = s.get(url, headers=headers, allow_redirects=True).text
    imgName = isbn + ".jpg"
    soup = bas(datailPage, "html5lib")
    try:
        imgUrl = soup.select("div#mainpic > a > img")[0].get("src")
        return downloadCover(s, imgUrl, imgName)
    except:
        isbnx = isbn.replace("-", "")
        imgUrl = "" + isbnx + ""
        proxies = {
            "http": "",
            "https": ""
        }
        return downloadCover(s, imgUrl, imgName, proxies)


def downloadCover(s, url, imgName, proxy=None):

    uaString = UAMaker().random_PC()
    headers = {
        "user-agent": uaString
    }

    imgName = imgName.replace("-", "")
    if(proxy):
        img = s.get(url, headers=headers, proxies=proxy)
    else:
        img = s.get(url, headers=headers)
    open("cover/"+imgName, "wb").write(img.content)

    return imgName

if __name__ == "__main__":
    finder = collection.find({"Cover": ""})
    for x in finder:
        isbnResult = x["ISBN"].strip()
        print(isbnResult)
        name = dban(isbnResult)
        id = {"_id": x["_id"]}
        coverData = {"$set": {"Cover": name, "ISBN": isbnResult}}
        collection.update_one(id, coverData)
        time.sleep(random.randint(3, 15))
