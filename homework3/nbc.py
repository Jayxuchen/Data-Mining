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
kVals={}
for k in trainData.keys():
    if k == classLabel:
        continue
    attSet=set()
    for v in trainData[k]:
        attSet.add(v)
        kVals[k]=len(attSet)
theSet = ['0','1']
for n in theSet:
    for v in trainData.keys():
        if v == classLabel:
            continue
        denom = sum(mles[n][v].values())
        for k in mles[n][v].keys():
            mles[n][v][k] = (mles[n][v][k] + 1)/(float(denom+kVals[v]))
            # print v+":"+k+":"+str(mles[n][v][k])
#use test data
result=[]
p_i={}
p_i['1']=[]
p_i['0']=[]
for i in range(len(testData[classLabel])):
    probZero=1;
    probOne=1;
    for k in testData.keys():
        if k == classLabel:
            continue
        observed = testData[k][i]
        if observed not in mles['0'][k] or observed not in mles['1'][k]:
            if observed not in trainData[k]:
                y_i = 0;
                for p in trainData[classLabel]:
                    if p == '0':
                        y_i=y_i+1
                probZero=probZero*1/float(y_i+kVals[k])
            if observed not in trainData[k]:
                y_i = 0;
                for p in trainData[classLabel]:
                    if p == '1':
                        y_i=y_i+1
                probOne=probOne *1/float(y_i+kVals[k])
        else:
            # print str(i) +": "+ k +":" +observed
            # print mles[y][k][observed]
            probZero = probZero * mles['0'][k][observed]
            probOne = probOne * mles['1'][k][observed]
    probZero=probZero*classPrior['0']
    p_i['0'].append(probZero/(probZero+probOne))
    probOne=probOne*classPrior['1']
    p_i['1'].append(probOne/(probZero+probOne))
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
squarecount=0
print p_i['0'][0]+p_i['1'][0]
print "SQUARED LOSS=" + str(((rows-wrongCount)/float(rows))**2/float(rows))
