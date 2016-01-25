__author__ = 'Anup'
from pymongo import MongoClient
import numpy as np
from sklearn.cluster import KMeans

fileFiltereduserilteredBusiness = open("C:\Users\Anup\Desktop\Smm Project\Yelp\FilteredCulturalBusiness.txt")
cityNameFiles=open("C:\Users\Anup\Desktop\Smm Project\Yelp\CityName.txt")
vectorFile=open("C:\Users\Anup\Desktop\Smm Project\Yelp\culturalVectorNormalized.txt")

filteredBusiness=[]
cityNames=[]
inputList=[]
for tuple in fileFiltereduserilteredBusiness:
    filteredBusiness.append(tuple.strip("\n").strip())

filteredBusiness=sorted(filteredBusiness)
#print filteredBusiness

client = MongoClient()
db = client['yelp']


"""
find={}
count=0
for city in collection.find(find):
    cityNameFiles.write(city["CityName"])
    cityNameFiles.write("\n")
    count+=1
    print count
"""

for city in cityNameFiles:
    name=city.replace("\n","")
    if name not in cityNames:
        cityNames.append(name)

cityNames=sorted(cityNames)
print cityNames


def initializeCityVector():
    vector={}
    for business in filteredBusiness:
        vector[business]=0

    return vector

def createCulturalVectorForCity(cityName,isNormalized):
    print "processing city "+cityName
    collection=db['clusterData']
    cityVector={}
    businessVector=initializeCityVector()
    totalReleventBusinessCount=0
    find={"CityName":cityName}
    for city in collection.find(find):
      reviewAndTip=city["reviewAndTips"]
      #print len(reviewAndTip)
      for instance in reviewAndTip:
          isCount=True
          businessCategoryList=instance["categories"]
          for cato in businessCategoryList:
              if businessVector.has_key(cato):
                  if isCount:
                      totalReleventBusinessCount+=1
                      isCount=False
                  count=businessVector[cato]
                  count+=1
                  businessVector[cato]=count

    print "Count "+str(totalReleventBusinessCount)
    if isNormalized:
      for key in businessVector:
        tempCount=businessVector[key]
        if tempCount!=0:
            tempCount=round((float(tempCount)/totalReleventBusinessCount)*100,3)
            businessVector[key]=tempCount
    cityVector[cityName]=businessVector

    return cityVector



def calCulturalVectorForCity(isNormalized):
    cityCulturalVector={}
    for city in cityNames:
        tempDict=createCulturalVectorForCity(city,isNormalized)
        cityCulturalVector.update(tempDict)
    return cityCulturalVector


#print createCulturalVectorForCity("Las Vegas",False)
#calCulturalVectorForCity(True)


def writeCulturalVector(isNormalized):
    vectorFile=open("C:\Users\Anup\Desktop\Smm Project\Yelp\culturalVectorNormalized.txt","w")
    cultVector=calCulturalVectorForCity(isNormalized)
    for city in cityNames:
        vect=cultVector[city]
        vectorString=city
        for business in filteredBusiness:
            vectorString=vectorString+","+str(vect[business])
        vectorFile.write(vectorString)
        vectorFile.write("\n")
    vectorFile.close()


def readVectorFile():
    for tuple in vectorFile:
        tempList=tuple.replace("\n","").split(",")
        inputList.append(tempList[1:])
    return inputList


def runKmens(K):
    data=np.array(readVectorFile())
    y_pred = KMeans(n_clusters=K).fit_predict(data)
    return y_pred

#print runKmens(11)
#writeCulturalVector(True)

def calFrequencyDistribution(K):
    lableVector=runKmens(K)
    freqDict={}
    count=0
    for lable in lableVector:
        if freqDict.has_key(lable):
            tempList=freqDict[lable]
            newList=np.array(map(float, inputList[count]))
            freqDict[lable]=newList+tempList
        else:
            freqDict[lable]=np.array(map(float, inputList[count]))
        count+=1
    """
    for lab in freqDict:
        print "Key "+str(lab),freqDict[lab]
    """
    return freqDict,lableVector

def createLable(K):
    frqDict,lableVect=calFrequencyDistribution(K)
    lableDict={}
    for key in frqDict:
        tempList=frqDict[key]
        high=0.001
        lable=[]
        count=0
        for value in tempList:
            if value>=high:
                if value==high:
                  lable.append(filteredBusiness[count])
                else:
                  lable[:]=[]
                  lable.append(filteredBusiness[count])
                high=value
            count+=1

        lableDict[key]=lable
    return lableDict,lableVect

#lable,bing=createLable(11)
#print lable

def assignLableToCities(K,noOfTime):
    cityLable={}
    for i in range(noOfTime):
        lables,lableVect=createLable(K)
        count=0
        for city in cityNames:
            if cityLable.has_key(city):
                lableList=cityLable[city]
                lableList=lableList+"-"+str(lables[lableVect[count]]).strip("[]").replace("'","")
                cityLable[city]=lableList
            else:
                cityLable[city]=""+str(lables[lableVect[count]]).strip("[]").replace("'","")

            count+=1
    return cityLable

def calFinalLable(K,noOfIteration):
    cityLable=assignLableToCities(K,noOfIteration)
    finalLable={}
    for city in cityLable:
        tempLableList=cityLable[city].split("-")
        lableCountList={}
        for lab in tempLableList:
            if lableCountList.has_key(lab):
                count=lableCountList[lab]
                count+=1
                lableCountList[lab]=count
            else:
                lableCountList[lab]=1
        high=1
        lable=[]
        for lableKey in lableCountList:
            if lableCountList[lableKey]>=high:
                if lableCountList[lableKey]==high:
                  lable.append(lableKey)
                else:
                  lable[:]=[]
                  lable.append(lableKey)
                high=lableCountList[lableKey]
        finalLable[city]=lable

    return finalLable

#calFrequencyDistribution(11)
#print assignLableToCities(11,11)
print calFinalLable(11,17)
"""
tempList=['Anthem',0,0,0,5,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,6,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1,0,0,0,0,3,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,1,0,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,4,0,0,0,0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,2,0,0]
print len(tempList)
print len(tempList[1:])
print tempList[1:]
"""
"""
tempList1=['1.1','0.0','1.0','2.0','4.0','8.0','0.0']
tempList2=['2.0','1.0','0.9','1.0','1.0','4.5','8.0']
modList1=map(float, tempList1)
modList2=map(float, tempList2)
print  np.array(modList1)+ np.array(modList2)
"""
#print round(1.3329,3)