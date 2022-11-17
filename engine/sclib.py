#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: sclib.py
# DATE: 2021/06/04
# TIME: 11:20:22

# DESCRIPTION: sclib

import requests
import math
import random
import os

from bs4 import BeautifulSoup as bas
from ua import UAMaker
from ic import covertISBN

scLibUrl = ""
frnUrl = ""
searchUrlHead = ""
searchUrlEnd = ""

def searchSCLib(isbn, proxy=None):
    
    bookInfoDict = {}
    series = ""

    sessionStr = str(math.ceil(random.random()*1000000000))

    uaString = UAMaker().random_PC()
    headers = {
        "user-agent": uaString
    }
    s = requests.session()
    if(proxy):
        s.proxies = proxy
    
    indexPage = s.get(frnUrl + sessionStr, headers=headers).content
    indexPageText = str(indexPage, "utf-8")
    
    soup = bas(indexPageText, "html5lib")
    tmp = soup.select("div#indexpage > form")
    actionUrl = tmp[0].get("action")

    jointSearchUrl = actionUrl + searchUrlHead + isbn + searchUrlEnd
    searchPage = s.get(jointSearchUrl, headers=headers).content

    searchPageText = str(searchPage, "utf-8")

    soup = bas(searchPageText, "html5lib")
    table = soup.select("table.items")
    if(len(table) != 0):
        if(len(table[0].find_all("div")) != 0):
            detailUrl = table[0].find_all("div")[0].find("a").get("href")
            detailPage = s.get(detailUrl).content

            detailPageText = str(detailPage, "utf-8")

            soup = bas(detailPageText, "html5lib")
            table = soup.select("div#details2")
            tr = table[0].find_all("tr")
            for x in tr:
                if(x.find("td").get_text().strip() == "ISBN"):
                    resultISBN = x.find_all("td")[1].get_text().split(":")[0].strip().replace("-", "")
                    if(isbn != resultISBN):
                        isbnNo = isbn
                    else:
                        isbnNo = resultISBN
                elif(x.find("td").get_text().strip() == "题名"):
                    title = x.find_all("td")[1].get_text().split("/")[0].strip()
                    title = "".join(title.split())
                    author = x.find_all("td")[1].get_text().split("/")[1].strip()
                    author = "".join(author.split())
                elif(x.find("td").get_text().strip() == "出版发行"):
                    press = x.find_all("td")[1].get_text().split(":")[1].strip().split(",")[0]
                    press = "".join(press.split())
                    site = x.find_all("td")[1].get_text().split(":")[0].strip()
                    site = "".join(site.split())
                    year = x.find_all("td")[1].get_text().split(",")[1].strip()
                    year = "".join(year.split())
                elif(x.find("td").get_text().strip() == "主题"):
                    classify = []
                    if("-" in x.find_all("td")[1].get_text()):
                        for subject in x.find_all("td")[1].get_text().split("-"):
                            subject = "".join(subject.split())
                            classify.append(subject.strip())
                    else:
                        tmp = x.find_all("td")[1].get_text()
                        tmp = "".join(tmp.split())
                        classify.append(tmp)
                elif(x.find("td").get_text().strip() == "分类号"):
                    CLCNo = x.find_all("td")[1].get_text().strip()
                elif(x.find("td").get_text().strip() == "丛编项"):
                    series = x.find_all("td")[1].get_text().strip()
                elif(x.find("td").get_text().strip() == "提要"):
                    synopsis = x.find_all("td")[1].get_text().strip()
                elif(x.find("td").get_text().strip() == "摘要"):
                    synopsis = x.find_all("td")[1].get_text().strip()
                
            bookInfoDict["Title"] = title
            bookInfoDict["Author"] = author
            bookInfoDict["Press"] = press
            bookInfoDict["Site"] = site
            bookInfoDict["Year"] = year
            bookInfoDict["Classify"] = classify
            bookInfoDict["CLCNo"] = CLCNo
            bookInfoDict["ISBN"] = isbnNo
            bookInfoDict["Series"] = series
            bookInfoDict["Synopsis"] = synopsis

            # CoverSrc = soup.select("div#uic_cover > img")[0].get("src")
            # CoverUrl = scLibUrl + CoverSrc
            # CoverName = str(isbn) + ".jpg"
            # downloadCover(s, CoverUrl, CoverName)
            
            bookInfoDict["Cover"] = ""
            bookInfoDict["Price"] = ""
            bookInfoDict["Rating"] = ""
            
            # print(bookInfoDict)
            return bookInfoDict
        else:
            return 404
    else:
        return 404


def downloadCover(s, url, imgName):

    uaString = UAMaker().random_PC()
    headers = {
        "user-agent": uaString
    }

    imgName = imgName.replace("-", "")

    img = s.get(url, headers)
    open("cover/"+imgName, "wb").write(img.content)