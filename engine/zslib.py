#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: zslib.py
# DATE: 2024/03/26
# TIME: 09:16:41

# DESCRIPTION:

import requests
import random

import isbnlib

from bs4 import BeautifulSoup as bas
from ua import UAMaker

zsLibBaseUrl = ""
searchUrlHead = ""
searchUrlEnd = ""


def searchZSLib(isbn, proxy=None):
    
    bookInfoDict = {}
    series = ""

    uaString = UAMaker().random_PC()

    headers = {
        "user-agent": uaString
    }
    s = requests.session()
    if(proxy):
        s.proxies = proxy
    
    indexResult = s.get(zsLibBaseUrl, headers=headers)
    indexResult.encoding = indexResult.apparent_encoding

    soup = bas(indexResult.text, "html5lib")
    actionUrl = soup.select_one("div#indexpage > form")["action"]

    searchURL = actionUrl + searchUrlHead + isbn + searchUrlEnd

    searchResult = s.get(searchURL, headers=headers)
    searchResult.encoding = searchResult.apparent_encoding

    soup = bas(searchResult.text, "html5lib")
    
    notRes = soup.select_one("div#feedbackbar").text.replace(" ", "")

    noTagFound = "没有搜索到任何匹配的记录。"

    if(notRes != noTagFound):
        trList = soup.select("div#details2 > table > tbody > tr")
        for x in trList:
            td1 = "".join(x.find_all("td")[0].text.split())
            if(td1 == "题名"):
                td2 = "".join(x.find_all("td")[1].select_one("a").text.split())
                title = td2.split("/")[0]
                author = td2.split("/")[1]
            if(td1 == "出版发行"):
                td2 = "".join(x.find_all("td")[1].select_one("a").text.split())
                site = td2.split(":")[0]
                press = td2.split(":")[1].split(",")[0]
                years = td2.split(":")[1].split(",")[1]
            
            if(td1 == "主题"):
                classify = "".join(x.find_all("td")[1].select_one("a").text.split()).split("-")

            if(td1 == "分类号"):
                CLCNo = "".join(x.find_all("td")[1].select_one("a").text.split())

            if(td1 == "ISBN"):
                isbn = isbnlib.get_canonical_isbn("".join(x.find_all("td")[1].select_one("a").text.split()))
            
            if(td1 == "丛编项"):
                series = "".join(x.find_all("td")[1].select_one("a").text.split())

                print(series)
    
        classify = list(set(classify))

        bookInfoDict["Title"] = title
        bookInfoDict["Author"] = author
        bookInfoDict["Press"] = press
        bookInfoDict["Site"] = site
        bookInfoDict["Year"] = years
        bookInfoDict["Classify"] = classify
        bookInfoDict["CLCNo"] = CLCNo
        bookInfoDict["ISBN"] = isbn
        bookInfoDict["Series"] = series
        bookInfoDict["Synopsis"] = ""


        bookInfoDict["Cover"] = ""
        bookInfoDict["Price"] = ""
        bookInfoDict["Rating"] = ""
        
        return bookInfoDict

    else:
        return 404
