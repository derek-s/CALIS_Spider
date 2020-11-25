from db import collection

isbn = "9787550226081"

bookInfoDict = {}
bookInfoDict["Title"] = "中国古代文化常识 : 插图修订第4版"
bookInfoDict["Author"] = "王力编著"
bookInfoDict["Press"] = "北京联合出版公司"
bookInfoDict["Site"] = "北京"
bookInfoDict["Year"] = "2014"
bookInfoDict["Classify"] = ['文化史', '古代', '中国']
bookInfoDict["CLCNo"] = "K220.3"

isbn_new = list(isbn)
isbn_new.insert(3, "-")
isbn_new.insert(5, "-")
isbn_new.insert(10, "-")
isbn_new.insert(15, "-")

bookInfoDict["ISBN"] = "".join(isbn_new)
# bookInfoDict["ISBN"] = isbn
collection.insert(bookInfoDict)