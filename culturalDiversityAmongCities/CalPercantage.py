__author__ = 'Anup'

vector="7	0	13	11	8	4	14	1"
arr=vector.split("\t")
#emoDict={"anticipation":0,"enjoyment":6.0,"sad":1,"disgust":1,"anger":1.5,"surprise":3,"fear":0,"trust":0}
def calPercentage(emoDict):
  keys=sorted(emoDict)
  #print keys
  sum=0.0
  convFloat=[]
  for i in sorted(emoDict):
    tempInt=float(emoDict[i])
    convFloat.append(tempInt)
    sum=sum+tempInt

  percentVector=[]
  count=0
  finalPerDict={}
  for i in convFloat:

    if i!=0:
        temp=(i/sum)*100
        #percentVector.append(temp)
        finalPerDict[keys[count]]=temp
    else:
        percentVector.append(i)
        finalPerDict[keys[count]]=i
    count+=1

  return finalPerDict

#print calPercentage(emoDict)


def calPercentageFromList(emoDict):
  keys=sorted(emoDict)
  #print keys
  sum=0.0
  convFloat=[]
  for i in emoDict:
    tempInt=float(i)
    convFloat.append(tempInt)
    sum=sum+tempInt

  percentVector=[]
  count=0
  finalPerDict={}
  for i in convFloat:

    if i!=0:
        temp=(float(i)/float(sum))*100
        percentVector.append(temp)
        finalPerDict[keys[count]]=temp
    else:
        percentVector.append(i)
        finalPerDict[keys[count]]=i
    count+=1

  print percentVector

calPercentageFromList(arr)