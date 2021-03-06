import requests
import re
import time
import random
from lxml import etree

from captcha import processPassKey
from ua import UAMaker

calisUrl = ""
queryUrl = ""
detailUrl = ""
checkUrl = ""
passKeyUrl = ""

def searchOpac(isbn, passkey, proxy):

    uaString = UAMaker().random_PC()

    headers = {
        "user-agent": uaString
    }
    headers_details = {
        "user-agent": uaString,
        "Referer": ""
    }

    print(isbn)
    queryPayload = {
        "actionType": 'doSimpleQuery',
        "pageno": '1',
        "pagingType": '0',
        "operation": 'searchRetrieve',
        "version": '1.1',
        "query": '(bath.isbn="' + isbn + '*")',
        "sortkey": 'title',
        "maximumRecords": '50',
        "startRecord": '1',
        "dbselect": 'all',
        "langBase": 'default',
        "conInvalid": '检索条件不能为空',
        "indexkey": 'bath.isbn|frt',
        "condition": isbn
        }

    detailPayload = {
        "actionType": "",
        "pagingType": "1",
        "operation": "searchRetrieve",
        "version": "1.1",
        "query": '(bath.isbn="' + isbn +'*")',
        "shw_cql": "ISBN = " + isbn + "*",
        "sortkey": "title",
        "groupkey": "null",
        "maximumRecords": 50,
        "startRecord": 1,
        "langBase": "null",
        "dbselect": "all",
        "searchlang": "null",
        "creator2": "null",
        "codetype": "null",
        "series2": "null",
        "unititle2": "null",
        "CLC2": "null",
        "datepublication": "null",
        "codelanguage": "null",
        "dbselect": "all",
        "queryType": 0,
        "fromTree": "false",
        "selInvalid": "请选择记录",
        "pageno": 1,
        "sortagainname":["title","title"],
        "pageno2": 1,
    }

    checkPayload = {
        "query": "（bath.isbn=“" + isbn + "*“）",
        "langBase": "null",
        "recIndex": 1,
        "recTotal": 1,
        "fullTextType": 1,
        "dbselect": "all",
        "queryType": 0,
        "curFullTextType": 1,
        "langBase4Holding": "null",
        "fromType4Holding": "null",
        "oid4Holding": "null",
        "id": "null",
        "userid": "null",
        "fullTextType": 1,
        "index": "null",
        "flag": "null",
        "subact": "check",
        "targetName": "alertWin",
        "jsfs6": "---选择地区中心---",
        "jsfs7": "---选择省中心---"
    }

    s = requests.session()
    if(len(proxy) != 0):
        s.proxies = proxy
    s.get(calisUrl)

    cookies = {"JSESSIONID":passkey}
    requests.utils.add_dict_to_cookiejar(s.cookies,cookies)
    r = s.post(queryUrl, data=queryPayload, headers=headers)
    selector = etree.HTML(r.text)
    notFound = selector.xpath("/html/body/table/tr/td/table/form/tr[1]/td/table/tr/td[2]/strong/font/text()")

    forbidden = selector.xpath("//title/text()")
    if("403" in forbidden[0]):
        print("403 forbidden")
        return 403
    else:
        if(len(notFound) == 0):
            # result = selector.xpath("/html/body/form[1]/table/tr/td/table/*")
            result = selector.xpath("/html/body/form[1]/table/tr/td/table/tr[6]/table/tr/td[2]/div/table[2]/tbody/tr")

            resultBooks = result[1:-1]
            bookInfoDict = {}
            bookInfo = resultBooks[0].xpath("td/a/text()")
            detailLink = resultBooks[0].xpath("td/a/@href")

            # print(bookInfo)

            pressText = "".join(resultBooks[0].xpath("td[4]/text()")).split()
            pressText = "".join(pressText)

            bookInfo = [x.strip() for x in bookInfo if x.strip()!='']

            bookInfoDict["Title"] = bookInfo[0].strip().split("/")[0]
            bookInfoDict["Author"] = bookInfo[1]

            bookInfoDict["Press"] = bookInfo[2]
            bookInfoDict["Site"] = pressText.split(":")[0]
            bookInfoDict["Year"] = pressText.split(",")[1]
            bookInfoDict["Cover"] = ""
            for eachLink in detailLink:
                if("javascript:doShowDetails" in eachLink):
                    detailArg = eachLink[25:-1].replace("'","").split(",")[4]
            r = s.post(detailUrl + detailArg, data=detailPayload, headers=headers_details)
            # print(r.text)
            # selector = etree.HTML(r.text)
            # result = selector.xpath("/html/body/div/table/tr/td/table/tr[4]/td/table  [7]/tbody/tr[7]/td[2]/a/text()")
            # print(result)
            # # print(etree.tostring(result[0]).decode("utf-8"))
            # bookInfoDict["classify"] = result[0].replace(" ", "").replace("--",",").  split(",")

            detailText = r.text
            pattern = r"验证码"
            finder = re.compile(pattern)
            passkeyTag = finder.findall(detailText)
            if(len(passkeyTag) == 0):
                return getDetails(detailText, bookInfoDict, isbn)
            else:
                print("Passkey find")
                flag = True
                while(flag):
                    r = s.get(passKeyUrl)
                    passkey = processPassKey(r.content)
                    checkPayload["passkey"] = passkey
                    headers_details = {
                        "user-agent": uaString,
                        "Referer": detailUrl + detailArg
                    }
                    r = s.post(checkUrl, data=checkPayload, headers=headers_details)
                    # print(r.text)
                    passkeyLoadText = r.text
                    pattern = r"当前检索条件"
                    finder = re.compile(pattern)
                    resultTag = finder.findall(passkeyLoadText)
                    if(len(resultTag) == 1):
                        print("find book")
                        flag = False
                        return getDetails(passkeyLoadText, bookInfoDict, isbn)
                    else:
                        print("passkey error try again")
                        time.sleep(random.randint(3, 15))
        else:
            return 404

def getDetails(detailText, bookInfoDict, isbn):
    pattern = r"\'calis.subject\'\,\'.*\'"
    finderSubject = re.compile(pattern)
    subjectString = finderSubject.findall(detailText)[0].replace("'", "")

    subjectString = subjectString.split(",")[1]
    
    if ("--" in subjectString):
        subjectList = subjectString.replace(" ", "").replace("--", ",").split(",")
        bookInfoDict["Classify"] = subjectList
    else:
        bookInfoDict["Classify"] = [subjectString]

    patternNo = r"\'bath.localClassification\'\,\'.*\'"
    finderCLCNo = re.compile(patternNo)
    CLCNoString = finderCLCNo.findall(detailText)[0].replace("'", "")
    CLCNoString = CLCNoString.split(",")[1]

    if CLCNoString.find("*"):
        CLCNoString = CLCNoString.replace("*", "")
    if CLCNoString.find(" "):
        CLCNoString = CLCNoString.replace(" ", ". ")
    bookInfoDict["CLCNo"] = CLCNoString

    isbn_new = list(isbn)
    isbn_new.insert(3, "-")
    isbn_new.insert(5, "-")
    isbn_new.insert(10, "-")
    isbn_new.insert(15, "-")
    bookInfoDict["ISBN"] = "".join(isbn_new)
    print(bookInfoDict)

    return bookInfoDict