__author__ = 'Anup'

from pymongo import MongoClient
import json

def readFile(path,databaseName,collectionName):
    file = open(path, 'r')
    client = MongoClient()
    db = client[databaseName]
    collection = db[collectionName]

    i = 0
    for line in file:
        #print line
        collection.insert_one(json.loads(line.strip().replace("\n",""))).inserted_id
        i = i + 1
        #if i == 10:
           # break
        print i
    file.close()
    client.close()


#path = "C:\Users\Anup\Desktop\Smm Project\Yelp\citytoBusiness.txt"
path="C:\Users\Anup\Desktop\Smm Project\Yelp\GroupedByCityAndBusiness.txt"
readFile(path,"yelp","clusteredData")
