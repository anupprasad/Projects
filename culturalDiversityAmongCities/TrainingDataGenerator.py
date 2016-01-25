__author__ = 'Anup'
from pymongo import MongoClient
import langdetect
from datetime import datetime
from langdetect import detect
import re
client = MongoClient()
db = client['yelp']
collection=db['businessData']
reviewData=db['reviewData']
#fileFiltereduser = open("C:\Users\Anup\Desktop\Smm Project\Yelp\FilteredUser.txt")
fileFiltereduserilteredBusiness = open("C:\Users\Anup\Desktop\Smm Project\Yelp\FilteredCulturalBusiness.txt")
reviewsFile=open("C:\Users\Anup\Desktop\Smm Project\Yelp\TrainingDataPositive.txt","w")
filteredUser = []
filteredBusiness = []

"""
for tuple in fileFiltereduser:
    filteredUser.append(tuple.strip("\n"))
"""
for tuple in fileFiltereduserilteredBusiness:
    filteredBusiness.append(tuple.strip("\n").strip())

def findReviewsWithstarRating(starRating,noOfReviews,languageCode):
  for filteredUser in  filteredBusiness:
    isFound=False
    find={"categories":{"$in":[filteredUser]}}
    businessList=[]
    count=0
    print "writing For Category "+filteredUser
    for len in collection.find(find):
       if count>=noOfReviews:
           break
       businessList.append(len["business_id"])
       count+=1

    for businessID in businessList:
        find={"business_id":businessID,"stars":starRating}
        count=0
        for review in reviewData.find(find):
             if count>=noOfReviews:
                 break
             line=re.sub('[@/#?]',"",review["text"].encode('utf-8').replace("\n",""))
             if line=="":
                 continue
             try:
               if detect(line)==languageCode:
                 reviewsFile.write(line)
                 reviewsFile.write("\n")
                 count+=1
             except (UnicodeDecodeError,langdetect.lang_detect_exception.LangDetectException):
                  continue
  reviewsFile.close()

findReviewsWithstarRating(5,10,'en')

#str="kkd @mddd mmnm/kkd  kd ????? dkjkdjnc # dkkd ."
"""
str="?????"
str2=re.sub('[@/#?]',"",str)

if str2=="":
    print "empty"
"""
