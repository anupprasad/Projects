__author__ = 'Anup'
#import langid
from pymongo import MongoClient
from datetime import datetime
import json
import sys
client = MongoClient()
db = client['yelp']
filteredUser = []
filteredBusiness = []
fileFiltereduser = open("C:\Users\Anup\Desktop\Smm Project\Yelp\FilteredUser.txt")
fileFiltereduserilteredBusiness = open("C:\Users\Anup\Desktop\Smm Project\Yelp\FilteredCulturalBusiness.txt")
#mergedResult=open("C:\Users\Anup\Desktop\Smm Project\Yelp\GroupedByCityAndBusiness.txt","a")

for tuple in fileFiltereduser:
    filteredUser.append(tuple.strip("\n"))

for tuple in fileFiltereduserilteredBusiness:
    filteredBusiness.append(tuple.strip("\n").strip())

"""
def readData():

    client = MongoClient()
    db = client['yelp']
    collection = db['businessData']
    pipeline=[{"$group":{"_id":"$city","businesscity":{"$sum":1}}}]
              #,{"$match":{"reviews":{"$gt":0}}}] # thh is is like select user_id ,count(*) group by user_id #having count(*)>20
    for line in collection.aggregate(pipeline) :
        print line
    client.close()
readData()
"""


def readData():
    collection = db['businessData']
    # ctgrp=[{"$group":{"_id":"$city","number of businesses":{"$sum":1}}}]
    pipeline = [{'$group': {'_id': '$city', 'businesses': {'$addToSet': '$business_id'}, 'count': {'$sum': 1}}}]
    for cur in collection.aggregate(pipeline):
        print cur
    client.close()

#if data has been inserted till record no 23 then pass 24 in record no to continue inserting from 24 onwards
def cityToBusinessReader(countThreshold,recordCount):
    collection = db['cityToBusiness']
    businessColl = db['businessData']
    reviewCol = db["reviewData"]
    tipCol = db["tipData"]
    clusterData=db["clusterData"]
    find = {"count": {"$gt": countThreshold}}
    count=0
    for record in collection.find(find):
        count+=1
        splitCount=0
        isSplited=False
        start= datetime.now()

        if  count<recordCount:
            continue

        print count

        cityName = record["city"]
        myDict={}
        myDict["CityName"]=cityName
        businessIdList = record["businesses"]
        totalReviewCount=0
        totalTipCount=0
        reviewAndTipList=[]
        for businesID in businessIdList:
           find = {"business_id": businesID}
           isFound = False
           reviewList = []
           tipList = []
           cato=[]

           for cur in businessColl.find(find):
            for culTureCategory in filteredBusiness:
                if isFound:
                    break
                for category in cur["categories"]:
                    if culTureCategory in category:
                        isFound = True
                        cato=cur["categories"]
                        break

            if isFound:
              isSplited=False
              reviewDict={}
              for cur in reviewCol.find(find):
                  if cur["user_id"] not in filteredUser:
                     reviewList.append(cur["review_id"])
                     #reviewList.append(cur["text"])
              totalReviewCount=totalReviewCount+len(reviewList)

              for cur in tipCol.find(find):
                if cur["user_id"] not in filteredUser:
                    tipList.append(cur["text"])
              totalTipCount=totalTipCount+len(tipList)

              reviewDict["BusinessId"]=businesID
              reviewDict["categories"]=cato
              reviewDict["ReviewCount"]=len(reviewList)
              reviewDict["TipCount"]=len(tipList)
              reviewDict["Reviews"]=reviewList
              reviewDict["Tips"]=tipList
              reviewAndTipList.append(reviewDict)
              #print "intermediate "+str(sys.getsizeof(reviewAndTipList))
              testDict={}
              testDict["test"]=reviewAndTipList
              x = json.dumps(testDict.__str__())
              sizeCount=sys.getsizeof(x)
              #print "Json size "+str(sizeCount)
              if 15300000-sizeCount<400000:
                  myDict["TotalReviewCount"]=totalReviewCount
                  myDict["TotalTipCount"]=totalTipCount
                  myDict["reviewAndTips"]=reviewAndTipList
                  n = json.dumps(myDict.__str__())
                  print "Size "+str(sys.getsizeof(n))
                  #mergedResult.write(str(myDict))
                  #mergedResult.write("\n")
                  clusterData.insert(myDict)
                  isSplited=True
                  myDict.clear()
                  reviewAndTipList[:]=[]
                  myDict["CityName"]=cityName
                  splitCount+=1
                  print "No of split "+str(splitCount)

        if not isSplited:
           myDict["TotalReviewCount"]=totalReviewCount
           myDict["TotalTipCount"]=totalTipCount
           myDict["reviewAndTips"]=reviewAndTipList
          # n = json.dumps(myDict.__str__())
           clusterData.insert(myDict)
        isSplited=False





        #print type(json.loads(myDict))
       # clusterData.insert(myDict)
       # clusterData.insert_one(json.dumps(myDict.__str__())).inserted_id
        #mergedResult.write("\n")
        client.close()
        end= datetime.now()
        print "Time Taken "+str(end-start)
   # mergedResult.close()






# readData()
#cityToBusinessReader(10,66)
"""
clusterData=db["clusterData"]

cToB=db['cityToBusiness']
find={"CityName":"Las Vegas"}
c=0
for i in clusterData.find(find):
     mergedResult.write(str(i).encode("utf-8"))
     mergedResult.write("\n")
     c+=1
     print c
"""


"""
emptyList=["one","jdjdjd","This is the second time we are going there with my husband, and I like their stakes but both times, found hair on my food."]
tempList=["one","two","three","jhkjhchx","This is the second time we are going there with my husband, and I like their stakes but both times, found hair on my food."]

print tempList
tempList[:]=[]
print tempList
"""


"""
if "threee" not in tempList:
    print "nahi Hai"
start= datetime.now()
print start
for i in range(100000):
    "hi"
end=datetime.now()
print end
print str(end-start)
"""

