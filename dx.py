#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: dx.py
# DATE: 2021/03/06
# TIME: 19:39:37

# DESCRIPTION: duxiu

import re
import time
import random
import requests
import hashlib
import os

from bs4 import BeautifulSoup as bss
from ua import UAMaker
from ic import covertISBN

duXiuUrl = ""
duXiuUrlHead = ""
duXiuUrlEnd = ""

duXiuDetailUrlHead = ""
duXiuDetailUrlMid = ""
duXiuDetailUrlEnd = ""

def searchDuxiu(isbn, proxy):
    """DuXiu Search"""
    bookInfoDict = {}
    uaString = UAMaker().random_PC()

    headers = {
        "user-agent": uaString
    }

    print(isbn)

    s = requests.session()
    if(len(proxy) != 0):
        s.proxies = proxy
    
    jointSearchUrl = duXiuUrlHead + str(isbn) + duXiuUrlEnd

    s.get(duXiuUrl, headers=headers)
    page = s.get(jointSearchUrl, headers=headers)
    pageText = page.text

    soup = bss(pageText, "html5lib")

    tmp = soup.select("div.books")
    if(len(tmp) != 0):
        tmp = soup.select(".divImg > a > img")
        if(len(tmp) != 0):
            coverUrl = tmp[0]["src"]
            picFileName = coverUrl.split("=")[1] + ".jpg"
            pic = s.get(coverUrl)
            with open(os.getcwd() + "/img/" + picFileName, "wb") as f:
                f.write(pic.content)
        tmp = soup.select("input#dxid0")
        if(len(tmp) != 0):
            dxID = tmp[0]["value"]
        tmp = soup.select("input#dxidskey")
        if(len(tmp) != 0):
            dxIDKey = tmp[0]["value"]
        duXiuDetailUrl = duXiuDetailUrlHead + dxID + duXiuDetailUrlMid  + dxIDKey    +duXiuDetailUrlEnd
        DetailsText = s.get(duXiuDetailUrl).text
        soup = bss(DetailsText, "html5lib")
        td = soup.select("td.view > table > tbody > tr > td > table >   tbody > tr > td")

        title = td[2].get_text()
        author = td[4].get_text()
        press = td[8].get_text().split("：")[1]
        site = td[8].get_text().split("：")[0]
        year = td[10].get_text()
        isbnNo = td[12].get_text()
        classify = []
        if("-" in td[14].get_text()):
            for subject in td[14].get_text().split("-"):
                classify.append(subject)
        else:
            classify.append(td[14].get_text())
        CLCNo = td[16].get_text()

        bookInfoDict["Title"] = title
        bookInfoDict["Author"] = author
        bookInfoDict["Press"] = press
        bookInfoDict["Site"] = site
        bookInfoDict["Year"] = year
        bookInfoDict["Classify"] = classify
        bookInfoDict["CLCNo"] = CLCNo
        bookInfoDict["ISBN"] = covertISBN(isbn)
        bookInfoDict["Cover"] = picFileName
        # print(bookInfoDict)
        return bookInfoDict
        # print(td[2].get_text(), td[4].get_text(), td[8].get_text(), td    [10].get_text(), td[12].get_text(), td[14].get_text(), td[16].  get_text())
    else:
        return 404
        


