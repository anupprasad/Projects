__author__ = 'Anup'

from pymongo import MongoClient
from copy import deepcopy



client = MongoClient()
db = client['yelp']
list=[]
businessList=[]
businessDict={}
def readData(fields,isForPrint):
    collection = db['reviewData']
    pipeline=[{"$group":{"_id":"$user_id","reviews":{"$sum":1}}},{"$match":{"reviews":{"$gt":1}}}] # this is is like select user_id ,count(*) group by user_id
                                                                                                     #having count(*)>20
    project={"_id":0,"text":1,"user_id":1}
    if len(fields)==0:
        print "please provide fields you want to print in the form ['All'] or ['Field1','Field2']"
        return

    i=0
    for line in collection.aggregate(pipeline):
     find={"user_id":line['_id']}
     for review in collection.find(find): # or can use collection.find(find,project)
        if fields[0]=='All':
           print review['user_id']+" : "+review['text']
        else:
            for att in fields:
                if isForPrint==True:
                   print review[att]
                else :
                    if list.__contains__(review[att]) :
                        print "dup found"
                    else :
                        list.append(review[att])

       #print line['_id']
    # i+=1
    # if i>1:
     # break

    print list.__sizeof__()

    client.close()


def countMaxReview():
    collection = db['reviewData']
    pipeline=[{"$group":{"_id":"$user_id","reviews":{"$sum":1}}},{"$match":{"reviews":{"$gt":20}}}] # thh is is like select user_id ,count(*) group by user_id

    project={"_id":0,"text":1,"user_id":1}                                                                                               #having count(*)>20

    i=0
    max=0
    userId='abcd'
    for line in collection.aggregate(pipeline):
         if max<line['reviews']:
             max=line['reviews']
             userId=line['_id']
         i+=1
         print i

    print "max review "+str(max)+ " For USER "+userId

    client.close()

def findUser(userID,collectionName,fields):
    collection = db[collectionName]
    find={"user_id":userID}
    for result in collection.find(find):
       if fields[0]==('All'):
           print result
       else :
           for attr in fields :
               print result[attr]
           print '\n'



def readBusiness(fields,isCount):
    collection = db['businessData']

    if len(list)==0:
        print "please populate global list first by calling readData()"
        return
    duplicate=0
    for businessid in list:
         find={"business_id":businessid}
         for result in collection.find(find):
             if len(fields)==0 or fields[0]=='All':
                 print result
             else:
                 for att in fields:
                   if isCount==False:
                     if businessList.__contains__(result[att]):
                         duplicate+=1
                         print duplicate
                     else :
                         businessList.append(result[att])
                   else:
                       if businessDict.has_key(result[att]):
                           count=businessDict[result[att]]
                           count+=1
                           businessDict[result[att]]=count
                           businessDict
                       else :
                            tempDict={result[att]:1}
                            businessDict.update(tempDict)


    print "Business length "+str(len(businessList))

    if isCount==True:
        print businessDict
    else:
        print businessList



def businessCategorizer():
    myDict2={}
    if len(businessList)==0:
        print "please populate businessList first"
        return
    for tuple in businessList:
       # print tuple
        for category in tuple:
           # print category
            if myDict2.__contains__(category):
                count=myDict2[category]
                count+=1
                myDict2[category]=count
            else:
                if len(myDict2)==0:
                    tempDict={category:1}
                    myDict2.update(tempDict)
                else :
                    isFound=False
                    key=myDict2.iterkeys()
                    copyDict=deepcopy(myDict2)
                    for temp in key:
                        if str(temp) in category or category in str(temp):
                            print "Key "+str(temp)+" category "+category
                            isFound=True
                            count=copyDict[str(temp)]
                            count+=1
                            copyDict[str(temp)]=count
                            break
                    if not isFound :
                        tempDict={category:1}
                        copyDict.update(tempDict)
                    myDict2=deepcopy(copyDict)

    print myDict2


def aggregateBusiness():
     allBusiness=[]
     collection = db['businessData']
     pipeline=[{"$group":{"_id":"$categories"}}]
     i=0
     for line in collection.aggregate(pipeline):
         allBusiness.append(line['_id'])

     print len(allBusiness)
     #print allBusiness
     print "please press Enter key"
     raw_input()
     businessCategorizer(allBusiness)


def businessCategorizer(business):
    myDict2={}
    for tuple in business:
       # print tuple
        for category in tuple:
           # print category
            if myDict2.__contains__(category):
                count=myDict2[category]
                count+=1
                myDict2[category]=count
            else:
                if len(myDict2)==0:
                    tempDict={category:1}
                    myDict2.update(tempDict)
                else :
                    isFound=False
                    key=myDict2.iterkeys()
                    copyDict=deepcopy(myDict2)
                    for temp in key:
                        if str(temp) in category or category in str(temp):
                            print "Key "+str(temp)+" category "+category
                            isFound=True
                            count=copyDict[str(temp)]
                            count+=1
                            copyDict[str(temp)]=count
                            break
                    if not isFound :
                        tempDict={category:1}
                        copyDict.update(tempDict)
                    myDict2=deepcopy(copyDict)

    print myDict2
    print len(myDict2)


readData(['user_id'],True)
#readBusiness(['categories'],False)
#businessCategorizer()#for this to work readBusiness should be run with False
#print businessList
#countMaxReview()
#aggregateBusiness()
#findUser("kGgAARL2UmvCcTRfiscjug","userData",['user_id','review_count'])# give ['All'] to print all fields




