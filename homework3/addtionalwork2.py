import csv, sys

classLabel = 'goodForGroups'

def setData(filename):
    trainingDataFilename =open(filename)
    reader = csv.reader(trainingDataFilename)
    headers = reader.next()
    data = {}
    for h in headers:
        data[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            if len(v) <1:
                data[h].append('BLANK')
            else:
                data[h].append(v)
    return data
trainData = setData('yelp2.csv')

classPrior={}
classPrior['0']=0;
classPrior['1']=0;
countzero=0;
countone=0;
for v in trainData[classLabel]:
    if v == '0':
        countzero=countzero+1;
    else:
        countone=countone+1;
classPrior['0']=countzero/float(countzero+countone)
classPrior['1']=countone/float(countzero+countone)
count = {}
count['0']={}
count['1']={}
for v in trainData.keys():
    if v == classLabel:
        continue
    count['1'][v]={}
    count['0'][v]={}
    for i,k in enumerate(trainData[v]):
        if(trainData[classLabel][i]=='1'):
            if k not in count['1'][v]:
                count['1'][v][k]=0;
            count['1'][v][k]+=1
        else:
            if k not in count['0'][v]:
                count['0'][v][k]=0;
            count['0'][v][k]+=1
kVals={}
for k in trainData.keys():
    if k == classLabel:
        continue
    attrSet=set()
    for v in trainData[k]:
        attrSet.add(v)
    kVals[k]=len(attrSet)
for k in count['1']['priceRange']:
    print k + " " + str(count['1']['priceRange'][k]) +" "+ str(sum(count['1']['priceRange'].values()))
for k in count['0']['priceRange']:
    print k + " " + str(count['0']['priceRange'][k]) +" "+ str(sum(count['1']['priceRange'].values()))
print kVals['priceRange']

atts = ['priceRange','alcohol','noiseLevel','attire']
for a in atts:
    for k,n in zip(count['1'][a],count['0'][a]):
        print "Smoothing"
        print "P("+a+"="+k+"|Y=1)= " + str(count['1'][a][k]+1)+"/"+str(sum(count['1']['priceRange'].values())+kVals[a])
        print "P("+a+"="+k+"|Y=0)= " + str(count['0'][a][k]+1)+"/"+str(sum(count['0']['priceRange'].values())+kVals[a])
        print "NO Smoothing"
        print "P("+a+"="+k+"|Y=1)= " + str(count['1'][a][k])+"/"+str(sum(count['1']['priceRange'].values()))
        print "P("+a+"="+k+"|Y=0)= " + str(count['0'][a][k])+"/"+str(sum(count['0']['priceRange'].values()))
