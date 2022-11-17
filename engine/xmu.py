#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: xmu.py
# DATE: 2021/06/04
# TIME: 09:41:27

# DESCRIPTION: xmu library 已废弃

import requests
import re

from ua import UAMaker
from bs4 import BeautifulSoup as bas
from lxml import etree, objectify

xmuUrl = ""
xmuUrlHead = ""
xmuUrlEnd = ""

xmuUrlRSSHead = ""
xmuUrlRSSEnd = ""

xmuDetailUrl = ""

def searchXMU(isbn, mode="rss", proxy=None):
    uaString = UAMaker().random_PC()

    headers = {
        "user-agent": uaString
    }

    print(isbn)

    s = requests.session()
    if(proxy):
        s.proxies = proxy
    
    if(mode == "rss"):
        jointSearchUrl = xmuUrlRSSHead + str(isbn) + xmuUrlRSSEnd
        page = s.get(jointSearchUrl, headers=headers)
        resultXmlStr = page.text
        # resultXmlTree = etree.fromstring(resultXmlStr.encode("utf-8"))
        unfoldTree = objectify.fromstring(resultXmlStr.encode("utf-8"))
        try:
            detailLink = unfoldTree.channel.item.link
        except:
            return 404
        detailPage = s.get(detailLink)
        return detailProcess(detailPage.text)

    else:
        jointSearchUrl = xmuUrlHead + str(isbn) + xmuUrlEnd
        page = s.get(jointSearchUrl, headers=headers)
        resultXmlStr = page.text

        soup = bas(resultXmlStr, "html5lib")
        searchResult = soup.select("ol#search_book_list")
        if(len(searchResult) == 0):
            return 404
        else:
            marcNo = searchResult[0].find("h3").find("a").get("href").split("=")[-1]
            detailLink = xmuDetailUrl + marcNo
            detailPage = s.get(detailLink)
            return detailProcess(detailPage.text)




def detailProcess(pageText):
    bookInfoDict = {}
    soup = bas(pageText, "html5lib")
    
    bookList = soup.select("dl.booklist")

    if(len(bookList) > 1):

        for x in bookList:
            if(x.find("dt").get_text() == "题名/责任者:"):
                title = x.find("dd").get_text().split("/")[0]
                author = x.find("dd").get_text().split("/")[1]
            elif(x.find("dt").get_text() == "出版发行项:"):
                press = x.find("dd").get_text().split(":")[1].split(",")[0]
                site = x.find("dd").get_text().split(":")[0]
                year = x.find("dd").get_text().split(":")[1].split(",")[1]
            elif(x.find("dt").get_text() == "ISBN及定价:"):
                isbnNo = x.find("dd").get_text().split("/")[0]
            elif(x.find("dt").get_text() == "学科主题:"):
                classify = []
                tmp = x.find("dd").get_text()
                if("-" in tmp):
                    for subject in tmp.split("-"):
                        classify.append(subject)
                else:
                    classify.append(tmp)
            elif(x.find("dt").get_text() == "中图法分类号:"):
                CLCNo = x.find("dd").get_text()

        bookInfoDict["Title"] = title
        bookInfoDict["Author"] = author
        bookInfoDict["Press"] = press
        bookInfoDict["Site"] = site
        bookInfoDict["Year"] = year
        bookInfoDict["Classify"] = classify
        bookInfoDict["CLCNo"] = CLCNo
        bookInfoDict["ISBN"] = isbnNo
        bookInfoDict["Cover"] = ""

        print(bookInfoDict)
        return bookInfoDict
    else:
        return 404