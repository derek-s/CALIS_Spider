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


def isNumber(str):
    try:
        float(str)
        return True
    except:
        return False

def exChangeRate(currency):
    """
    currency exchange
    """

    url = "" + currency
    uaString = UAMaker().random_PC()
    headers = {
        "user-agent": uaString
    }
    resultJson = requests.get(url)
    return resultJson.json()["rates"]


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

    # Book Cover
    imgUrl = soup.select("div#mainpic > a > img")[0].get("src")
    
    # Book Price 2021-06-26
    infoSpan = soup.select("div#info > span")
    si = -1
    for spanindex, info in enumerate(infoSpan):
        if(info.text == "定价:"):
            si = spanindex
    if(si != -1):
        price = (soup.select("div#info > span")[si].next_sibling).strip()
        if(isNumber(price)):
            pass
        elif("元" in price):
            price = price.replace("元", "")
        elif("CNY" in price):
            price = price.replace("CNY", "").replace(" ", "")
        else:
            priceList = price.split(" ")
            currency = priceList[0]
            oriPrice = priceList[1]
            if("," in oriPrice):
                oriPrice = oriPrice.replace(",", ".")
            exRateCNY = exChangeRate(currency)["CNY"]
            price = float(oriPrice) * exRateCNY
    else:
        price = 0
    print(price)
    price = format(float(price), ".2f")
    return downloadCover(s, imgUrl, imgName), price
    # return price, imgUrl
    


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
        coverFileName, price = dban(isbnResult)
        id = {"_id": x["_id"]}
        coverData = {"$set": {"Cover": coverFileName, "ISBN": isbnResult, "Price": price}}
        collection.update_one(id, coverData)
        time.sleep(random.randint(3, 15))
