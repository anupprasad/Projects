__author__ = 'Anup'
import operator
fileToWriteForAllCity=open("C:\Users\Anup\Desktop\Smm Project\Yelp\LanguageCountForAllCity.txt")
languaheMapperPath=open("C:\Users\Anup\Desktop\Smm Project\Yelp\languageMapper.txt")
langOutPut=open("C:\Users\Anup\Desktop\Smm Project\Yelp\languageFrequencyDistribution.csv","w")

langDict={}
for lang in languaheMapperPath:
    arr=lang.split("\t")
    langDict[arr[1].lower().replace("\n","")]=arr[0]


for line in fileToWriteForAllCity:
    arr=line.split("{")
    langOutPut.write("\n")
    langOutPut.write("\n")
    city=arr[0]
    string=arr[1].replace("}","").replace("\"","").replace("\n","")
    str2=string.split(",")
    myDict={}
    langOutPut.write(city)
    langOutPut.write("\n")
    print city
    count2=0
    for lang in str2:
        count=lang.split(":")

        if count[0].replace("'","").replace("\"","").strip()!='en':
           myDict[count[0].replace("'","").replace("\"","")]=int(count[1])
           count2=count2+int(count[1])
    sorted_myDict = sorted(myDict.items(), key=operator.itemgetter(1))
    #print sorted_myDict[-5:]
    finalDict={}
    for i in sorted_myDict[-5:]:
        try:
            finalDict[langDict[(i[0]).strip()]]=(float(i[1])/count2)*100
            langOutPut.write(langDict[(i[0]).strip()]+","+str((float(i[1])/count2)*100))
            langOutPut.write("\n")
        except ZeroDivisionError,KeyError:
            print

    print finalDict
