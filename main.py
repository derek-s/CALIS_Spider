import csv
import time
import random
import argparse
import datetime

from db import collection

from engine.calis import searchOpac
from engine.sclib import searchSCLib
from engine.nlc import searchNLC

from ic import covertISBN

parser = argparse.ArgumentParser(description="Books MetaData Spider")
parser.add_argument("--target", "-t", help="Target Website dx or calis default = calis", default="calis", required=True)
args = parser.parse_args()

# proxy config
proxy_ip = ""
username = ""
password = ""
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
}

def getDate(): 
    """
        get now date
    """
    today = datetime.date.today().strftime("%Y-%m-%d")
    return today



if __name__ == "__main__":

    csvFile = open("isbn.csv", "r")
    notFoundFile = open("notfound.csv", "a+")
    reader = csv.reader(csvFile)

    if(args.target == "calis"):
        # reader = ['978-7-80236-780-7']
        for item in reader:
            isbn_new = covertISBN(item[0])
            count = collection.count_documents({"ISBN": isbn_new})
            if(count == 0):
                result = searchOpac(item[0], "cmhbmv245irg")
                # result = searchOpac(item[0], "aiezkqxk6tjx", proxies)
                # result = searchOpac(item[0], "jxdfyqxku8hq", proxies)

                if type(result) != int:
                    print("find write db")
                    result["addTime"] = getDate()
                    print(result)
                    collection.insert_one(result)
                    time.sleep(random.randint(3, 15))
                if result == 404:
                    print("notFound")
                    notFoundFile.write(item[0] + "\n")
                    time.sleep(random.randint(3, 15))
            else:
                print("in base")
    
    elif(args.target == "sclib"):
        for item in reader:
            isbn_new = covertISBN(item[0])
            count = collection.count_documents({"ISBN": isbn_new})
            if(count == 0):
                result = searchSCLib(isbn_new)
                if type(result) != int:
                    print("find, write db")
                    result["addTime"] = getDate()
                    print(result)
                    collection.insert_one(result)
                    time.sleep(random.randint(3, 15))
                if result == 404:
                    print("notFound")
                    notFoundFile.write(item[0] + "\n")
                    time.sleep(random.randint(3, 15))
            else:
                print("in base")
    elif(args.target == "nlc"):
        for item in reader:
            isbn_new = covertISBN(item[0])
            count = collection.count_documents({"ISBN": isbn_new})
            if(count == 0):
                result = searchNLC(isbn_new)
                if type(result) != int:
                    print("find, write db")
                    result["addTime"] = getDate()
                    print(result)
                    collection.insert_one(result)
                    time.sleep(random.randint(3, 15))
                if result == 404:
                    print("notFound")
                    notFoundFile.write(item[0] + "\n")
                    time.sleep(random.randint(3, 15))
            else:
                print("in base")


    else:
        print("you need chose website")