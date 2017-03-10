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
target = open("test.txt", 'w')
classPrior={'0','1'}
for v in trainData['classLabel']:
    if v == '0':
        classPrior['0'] = classPrior['0']+1
    else:
        classPrior['1'] = classPrior['1']+1
print(classPrior)
for v in trainData.keys():
    if v == classLabel:
        continue
    for i,k in enumerate(trainData[v]):
        if(trainData[classLabel][i]=='1'):
            continue
