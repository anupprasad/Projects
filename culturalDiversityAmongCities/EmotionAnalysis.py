__author__ = 'Anup'

from pymongo import MongoClient
import EmotionParser as emp
import CalPercantage as per
import LanguageClassifier as languageClassify
client = MongoClient()
db = client['yelp']
emoOutPath=open("C:\Users\Anup\Desktop\Smm Project\Yelp\CityEmotion.csv","a")
emotionOrderList=['anger', 'anticipation', 'disgust', 'enjoyment', 'fear', 'sad', 'surprise', 'trust']

emoOutPath.write("\n")
def readReview(cityName):
    clusterData=db["clusterData"]
    businessDict={}
    find={"CityName":cityName}
    for city in clusterData.find(find):
        bsusinessList=city["reviewAndTips"]
        for business in bsusinessList:
            if businessDict.has_key(str(business["categories"])):
                reviewList=[]
                reviewList=businessDict[str(business["categories"])]
                reviewList.append(business["Reviews"])
                businessDict[str(business["categories"])]=reviewList
            else:
               businessDict[str(business["categories"])]=business["Reviews"]
    return businessDict


def emoDetection(cityName):
    businseeCluster=readReview(cityName)
    reviewCursor=db["reviewData"]
    emotionDict={}
    for catogary in businseeCluster:
        emoList=[]
        print "Evaluating ",catogary
        reviewList=businseeCluster[catogary]
        for reviewId in reviewList:
            find={"review_id":reviewId}
            for rev in reviewCursor.find(find,no_cursor_timeout=True):
                review=rev["text"]
                langType=languageClassify.detectLanguage(review)
                if langType=='en':
                  tempEmoDict=emp.consolodateResult(review)
                  emoList.append(tempEmoDict)
                else:
                    print langType

        emotionDict[catogary]=emoList
    return emotionDict



def createConsolidatedResult(cityName):
    myDict=emoDetection(cityName)
    emoOutPath.write(cityName)
    for emotionCat in emotionOrderList:
       emoOutPath.write(","+emotionCat)
    emoOutPath.write("\n")

    for key in myDict:
        tempEmoDict={}
        emoOutPath.write(key.replace(",","").replace("u",""))
        listOfEmot=myDict[key]
        for emoVector in listOfEmot:
            for emoKey in emoVector:
                if tempEmoDict.has_key(emoKey):
                    count=tempEmoDict[emoKey]
                    count=count+emoVector[emoKey]
                    tempEmoDict[emoKey]=count
                else:
                    tempEmoDict[emoKey]=emoVector[emoKey]

        tempEmoPerDict=per.calPercentage(tempEmoDict)
        for emoDist in sorted(tempEmoPerDict):
            emoOutPath.write(","+str(tempEmoPerDict[emoDist]))
        emoOutPath.write("\n")

createConsolidatedResult("Anthem")

