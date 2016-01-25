__author__ = 'Anup'
import re
import langdetect
from pymongo import MongoClient
from langdetect import detect

fileToWrite=open("C:\Users\Anup\Desktop\Smm Project\Yelp\LanguageCount.txt","w")
fileToWriteForAllCity=open("C:\Users\Anup\Desktop\Smm Project\Yelp\LanguageCountForAllCity.txt","a")
cityNameFiles=open("C:\Users\Anup\Desktop\Smm Project\Yelp\CityName.txt")
errorReview=open("C:\Users\Anup\Desktop\Smm Project\Yelp\Error.txt","a")
def splitReview(review):
    line=re.sub('[@/#?*]',"",review.encode('utf-8').replace("\n",""))
    stoper=[".","!","?"]
    for stop in stoper:
        if stop in line:
            list=line.split(stop)
            for sen in list:
                if len(sen)>10:
                    return sen

    return line



def detectLanguage(text):
     sent=splitReview(text)
     language="lol"
     try:
          language=detect(sent)

     except(UnicodeDecodeError,langdetect.lang_detect_exception.LangDetectException):
          print "detect error",UnicodeDecodeError.message
          errorReview.write(sent)
          errorReview.write("\n")
     return language


#Call this method to find language distribution for individual city.
def getReviews(cityName,recordToSkip):
    client = MongoClient()
    db = client['yelp']
    cluster=db["clusterData"]
    review=db["reviewData"]
    langDict={}
    find={"CityName":cityName}
    for city in cluster.find(find,no_cursor_timeout=True):
        reviewAndTipList=city["reviewAndTips"]
        businessCount=0
        for business in reviewAndTipList:
            businessCount+=1
            if businessCount<recordToSkip:
                continue
            # print "Business Count ",businessCount
            reviewIdList=business["Reviews"]
            for reviewID in reviewIdList:

                findReview={"review_id":reviewID}
                for re in review.find(findReview,no_cursor_timeout=True):
                    rev=re["text"]
                    sent=splitReview(rev)
                    try:
                       language=detect(sent)
                       if langDict.has_key(language):
                           count=langDict[language]
                           count+=1
                           langDict[language]=count
                       else:
                           langDict[language]=1
                    except (UnicodeDecodeError,langdetect.lang_detect_exception.LangDetectException):
                        print "detect error",UnicodeDecodeError.message
                        errorReview.write(sent)
                        errorReview.write("\n")
            #fileToWrite.write(str(langDict))
            #fileToWrite.write("\n")

    client.close()

    return langDict

#Call this method to find language distribution for individual city.
#print getReviews("Paradise Valley",0)


#Call this method to find language distribution for entire city
def detectLanguageOfCities(noOfCityToSkip):
    cityNames=[]
    fileToWriteForAllCity.write("==================================================================")
    fileToWriteForAllCity.write("\n")
    for city in cityNameFiles:
       name=city.replace("\n","")
       if name not in cityNames:
         cityNames.append(name)

    cityNames=sorted(cityNames)
    count=0
    for city in cityNames:
        count+=1
        if count<=noOfCityToSkip:
            continue
        print "City Count ",count
        languageDict=getReviews(city,0)
        fileToWriteForAllCity.write(city+" "+str(languageDict))
        fileToWriteForAllCity.write("\n")
    fileToWriteForAllCity.close()
    cityNameFiles.close()
    fileToWrite.close()
    errorReview.close()


#detectLanguageOfCities(15)