__author__ = 'Anup'

from pymongo import MongoClient
from copy import deepcopy
client = MongoClient()
db = client['yelp']

orderList=[]
def aggregateOnReviewCount():
    file=open("C:\Users\Anup\Desktop\Smm Project\Yelp\ReviewCount.txt",'w')
    collection = db['reviewData']

    myDict={}
    pipeline=[{"$group":{"_id":"$user_id","reviews":{"$sum":1}}},{"$match":{"reviews":{"$gt":600}}}] # this is is like select user_id ,count(*) group by user_id
    for line in collection.aggregate(pipeline):

        file.write(line["_id"]+" : "+str(line["reviews"]))
        file.write("\n")

        if myDict.has_key(line["reviews"]):
            count=myDict[line["reviews"]]
            count+=1
            myDict[line["reviews"]]=count
        else:
            myDict[line["reviews"]]=1
            orderList.append(line["reviews"])

    file.close()
    return myDict



myDict=aggregateOnReviewCount()
sorted(orderList)
#print orderList

for key in orderList:
   print str(key)+" : "+str(myDict[key])