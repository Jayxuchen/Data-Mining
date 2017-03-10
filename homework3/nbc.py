import csv, sys

classLabel = 'goodForGroups'
if len(sys.argv) != 3:
    print("invalid number of arguments : correct usage \"python nbc.py train-set.csv test-set.csv\"")
    exit()
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
trainData = setData(sys.argv[1])
testData = setData(sys.argv[2])
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
mles = {}
mles['0']={}
mles['1']={}
for v in trainData.keys():
    if v == classLabel:
        continue
    mles['1'][v]={}
    mles['0'][v]={}
    for i,k in enumerate(trainData[v]):
        if(trainData[classLabel][i]=='1'):
            if k not in mles['1'][v]:
                mles['1'][v][k]=0;
            mles['1'][v][k]=mles['1'][v][k]+1
        else:
            if k not in mles['0'][v]:
                mles['0'][v][k]=0;
            mles['0'][v][k]=mles['0'][v][k]+1
theSet = ['0','1']
for n in theSet:
    for v in trainData.keys():
        if v == classLabel:
            continue
        denom = sum(mles[n][v].values())
        for k in mles[n][v].keys():
            mles[n][v][k] = mles[n][v][k]/float(denom)
            # print v+":"+k+":"+str(mles[n][v][k])
#use test data
result=[]
for i in range(len(testData[classLabel])):
    prob=1;
    for k in testData.keys():
        if k == classLabel:
            continue
        observed = testData[k][i]
        y = testData[classLabel][i]
        if observed not in mles[y][k]:
            #dosomething
            continue
        else:
            print str(i) +": "+ k +":" +observed
            print mles[y][k][observed]
            prob = prob * mles[y][k][observed]
    prob=prob*classPrior[y]
    result.append(prob)
for i,k in enumerate(result):
    print str(i)+":" +str(k)
