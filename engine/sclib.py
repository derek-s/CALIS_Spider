#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: sclib.py
# DATE: 2023/05/27

# DESCRIPTION: sclib

import requests
import math
import random
import os

from bs4 import BeautifulSoup as bas
from ua import UAMaker
from ic import covertISBN

scLibUrl = ""
searchUrlHead = ""
searchUrlEnd = ""

detailUrlHead = ""
detailUrlMid = ""
detailUrlMidA = ""
detailUrlEnd = ""

def searchSCLib(isbn, proxy=None):
    
    bookInfoDict = {}
    series = ""

    uaString = UAMaker().random_PC()
    headers = {
        "user-agent": uaString
    }
    s = requests.session()
    if(proxy):
        s.proxies = proxy
    
    searchURL = scLibUrl + searchUrlHead + isbn + searchUrlEnd

    searchResult = s.get(searchURL, headers=headers).text

    soup = bas(searchResult, "html5lib")
    
    notResArea = soup.select_one(".notResArea")

    if(notResArea == None):

        libBookLi = soup.select_one(".libBookUl")
        
        detailA = libBookLi.select_one("div.rankLiIn > div.rankInCon.clearfix > div.overHide > a")

        href = detailA["href"]

        bookDetailID = href.split("(")[-1].split(",")[0]

        detailUrl = scLibUrl + detailUrlHead + bookDetailID + detailUrlMid + isbn + detailUrlMidA + isbn + detailUrlEnd

        detailPage = s.get(detailUrl, headers=headers).text

        soup = bas(detailPage, "html5lib")

        bkTxt = soup.select_one(".bkTxt")

        title = bkTxt.select_one(".bkTxtTit").get_text().strip()

        bkTxtLeftLi = bkTxt.select("div.bkTxtLeft > ul > li")
        bkTxtRightLi = bkTxt.select("div.bkTxtRight > ul > li")
        detailArray = []
        classify = []
        for x in bkTxtLeftLi:
            detailArray.append(x.get_text().strip().split())
        
        for y in bkTxtRightLi:
            detailArray.append(y.get_text().strip().split())
        
        for z in detailArray:

            bField = z[0]

            if(bField == "出版发行："):
                site = z[1]
                press = z[2].split("，")[0]
                year = z[3]
            if(bField == "主要责任者："):
                author = z[1]
            if(bField == "主题词："):
                for m in z:
                    if(m != "主题词："):
                        classify.append(m)
            if(bField == "中图分类法："):
                CLCNo = z[1]
        
        classify = list(set(classify))

        
        bookInfoDict["Title"] = title
        bookInfoDict["Author"] = author
        bookInfoDict["Press"] = press
        bookInfoDict["Site"] = site
        bookInfoDict["Year"] = year
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