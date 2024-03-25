#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: shlib.py
# DATE: 2024/03/25
# TIME: 22:39:20

# DESCRIPTION:

import requests

from bs4 import BeautifulSoup as bas
from ua import UAMaker

shLibUrl = ""
searchUrlHead = ""
searchUrlEnd = ""


def searchSHLib(isbn, proxy=None):
    
    bookInfoDict = {}
    series = ""

    uaString = UAMaker().random_PC()

    headers = {
        "user-agent": uaString
    }
    s = requests.session()
    if(proxy):
        s.proxies = proxy
    
    searchURL = shLibUrl + searchUrlHead + isbn + searchUrlEnd

    searchResult = s.get(searchURL, headers=headers).text

    soup = bas(searchResult, "html5lib")
    
    notResArea = soup.find("div", {"class": "search-stats"}).find("h2")

    if(notResArea == None):
        detailUrl = shLibUrl + soup.select_one(".result-body > div > a")["href"]
        detailText = s.get(detailUrl, headers=headers).text
        soup = bas(detailText, "html5lib")
        content = soup.select_one("div#content").find("div", {"class": "media-body"})
        
        metaTable = content.select_one("table#table-detail")
        metaTh = metaTable.find_all("th")

        for index, domElement in enumerate(metaTh):
            if(domElement.text == "Main Authors:"):
                author = metaTable.find_all("td")[index].select_one("span.author-property-role").text[1:-1].replace(" ", "").replace("\n", "")
            if(domElement.text == "Published:"):
                press = metaTable.find_all("td")[index].text.replace(" ", "").replace("\n", "")
            if(domElement.text == "Publisher Address:"):
                site = metaTable.find_all("td")[index].text.replace(" ", "").replace("\n", "")
            if(domElement.text == "Publication Dates:"):
                year = metaTable.find_all("td")[index].text.replace(" ", "").replace("\n", "")
            if(domElement.text == "Subjects:"):
                classify = metaTable.find_all("td")[index].text.replace(" ", "").replace("\n", "").split(">")
            if(domElement.text == "CLC:"):
                CLCNo = metaTable.find_all("td")[index].text.replace(" ", "").replace("\n", "")
            if(domElement.text == "ISBN:"):
                isbn = metaTable.find_all("td")[index].text.replace(" ", "").replace("\n", "").replace("-", "")
            if(domElement.text == "Series:"):
                series = metaTable.find_all("td")[index].text.replace(" ", "").replace("\n", "")
        
        title = content.select_one("h3").text

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

