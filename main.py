import csv
import time
import random

from db import collection
from calis import searchOpac

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
    # reader = ['9787121177408']
    for item in reader:
        isbn_new = list(item[0])
        isbn_new.insert(3, "-")
        isbn_new.insert(5, "-")
        isbn_new.insert(10, "-")
        isbn_new.insert(15, "-")
        isbn_new = "".join(isbn_new)
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