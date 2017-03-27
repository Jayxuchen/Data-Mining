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

mle = {}
theSet = ['0','1']
for n in theSet:
    mle[n]={}
    for v in trainData.keys():
        if v == classLabel:
            continue
        mle[n][v]={}
        denom = sum(count[n][v].values())
        for k in count[n][v].keys():
            mle[n][v][k] = (count[n][v][k] + 1)/(float(denom+kVals[v]))
#use test data
result=[]
p_i={}
p_i['1']=[]
p_i['0']=[]
for i in range(len(testData[classLabel])):
    probZero=1;
    probOne=1;
    for attr in testData.keys():
        if attr == classLabel:
            continue
        observed = testData[attr][i]
        if observed not in mle['0'][attr]:
            y_i = 0;
            for p in trainData[classLabel]:
                if p == '0':
                    y_i+=1
            probZero=probZero*1/float(y_i+kVals[attr])
        else:
            probZero = probZero * mle['0'][attr][observed]

        if observed not in mle['1'][attr]:
            y_i = 0;
            for p in trainData[classLabel]:
                if p == '1':
                    y_i+=1
            probOne=probOne *1/float(y_i+kVals[attr])
        else:
            probOne = probOne * mle['1'][attr][observed]

    probZero=probZero*classPrior['0']
    probOne=probOne*classPrior['1']
    denom = probZero+probOne
    p_i['0'].append(probZero/denom)
    p_i['1'].append(probOne/denom)
    if probZero > probOne:
        result.append('0')
    else:
        result.append('1')

rows = len(testData[classLabel])
wrongCount = 0
for i,k in enumerate(result):
    if(testData[classLabel][i]!=k):
        wrongCount=wrongCount+1
print "ZERO-ONE LOSS="+str(wrongCount/float(rows))
squareCount=0
i = 0
for j,k in zip(p_i['1'],p_i['0']):
    subval = 1 - float(testData[classLabel][i]) * j - (1-float(testData[classLabel][i])) * k
    squareCount = squareCount+subval**2
    i+=1

print "SQUARED LOSS=" + str(squareCount/float(rows))
