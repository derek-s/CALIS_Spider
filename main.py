import csv
import time
import random
import argparse

from db import collection
from calis import searchOpac
from dx import searchDuxiu
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



if __name__ == "__main__":

    csvFile = open("isbn.csv", "r")
    notFoundFile = open("notfound.csv", "a+")
    reader = csv.reader(csvFile)

    if(args.target == "calis"):
        # reader = ['978-7-80236-780-7']
        for item in reader:
            isbn_new = covertISBN(item[0])
            count = collection.find({"ISBN": isbn_new})
            if(count.count() == 0):
                result = searchOpac(item[0], "cmhbmv245irg", "")
                # result = searchOpac(item[0], "aiezkqxk6tjx", proxies)
                # result = searchOpac(item[0], "jxdfyqxku8hq", proxies)

                if type(result) != int:
                    print("find write db")
                    print(result)
                    collection.insert(result)
                    time.sleep(random.randint(3, 15))
                if result == 404:
                    print("notFound")
                    notFoundFile.write(item[0] + "\n")
                    time.sleep(random.randint(3, 15))
            else:
                print("in base")
    elif(args.target == "dx"):
        for item in reader:
            isbn_new = covertISBN(item[0])
            count = collection.find({"ISBN": isbn_new})
            if(count.count() == 0):
                result = searchDuxiu(isbn_new, "")
                if type(result) != int:
                    print("find write db")
                    print(result)
                    collection.insert(result)
                    time.sleep(random.randint(3, 15))
                if result == 404:
                    print("notFound")
                    notFoundFile.write(item[0] + "\n")
                    time.sleep(random.randint(3, 15))
            else:
                print("in base")

    else:
        print("you need chose website")