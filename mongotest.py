from pymongo import MongoClient
from config import Config

cl = MongoClient(Config.MONGO_URI)
db = cl.testdb
col = db.col1
x = col.find_one()
print('in mngo')
print(x)
