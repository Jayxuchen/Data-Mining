import csv, sys

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
            data[h].append(v)
    return data
trainData = setData('train-set1.csv')
testData = setData('test-set1.csv')

#1c
count = 0
for v in trainData['goodForGroups']:
     if v=='1':count+=1
p_yes=count/float(len(trainData['goodForGroups']))
p_no=1-p_yes
print(p_yes)
print(p_no)
