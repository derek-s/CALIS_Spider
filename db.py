from pymongo import MongoClient

DB_HOSTS = "127.0.0.1"
DB_PORT = 27017
DB_USERNAME = ""
DB_PWD = ""


client = MongoClient(host=DB_HOSTS, port=DB_PORT, username=DB_USERNAME, password=DB_PWD, authSource="Library")
db = client.get_database("Library")
collection = db.books
