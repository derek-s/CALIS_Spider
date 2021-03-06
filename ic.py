#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# AUTHOR: Derek Song
# FILE: ic.py
# DATE: 2021/03/06
# TIME: 22:03:00

# DESCRIPTION: convert isbn to standard

def covertISBN(isbn):
    if(len(isbn) == 13):
        allNumberISBN = str(isbn).replace("-", "")
        newISBN = list(allNumberISBN)
        newISBN.insert(3, "-")
        newISBN.insert(5, "-")
        newISBN.insert(10, "-")
        newISBN.insert(15, "-")
        newISBN = "".join(newISBN)

        return newISBN
    elif(len(isbn) == 10):
        allNumberISBN = str(isbn).replace("-", "")
        newISBN = list(allNumberISBN)
        newISBN.insert(1, "-")
        newISBN.insert(6, "-")
        newISBN.insert(11, "-")
        newISBN = "".join(newISBN)
        return newISBN
    else:
        return isbn

