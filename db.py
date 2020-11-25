from pymongo import MongoClient

DB_HOSTS = "127.0.0.1"
DB_PORT = 27017
DB_USERNAME = ""
DB_PWD = ""


client = MongoClient(DB_HOSTS, DB_PORT)
db = client.Library
collection = db.books
db.authenticate(DB_USERNAME, DB_PWD)