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
            if len(v) <1:
                data[h].append('BLANK')
            else:
                data[h].append(v)
    return data
trainData = setData('train-set1.csv')
testData = setData('test-set1.csv')
print(len(trainData['goodForGroups']))
print(len(testData['goodForGroups']))
#1c
count = 0
for v in trainData['goodForGroups']:
     if v=='1':count+=1
p_yes=str(count)+ "/" +str(len(trainData['goodForGroups']))
p_no= str(len(trainData['goodForGroups'])-count) + "/" + str(len(trainData['goodForGroups']))
print(p_yes)
print(p_no)
p_yes_laplace=(count+1)/(float(len(trainData['goodForGroups']))+2)
p_no_laplace =1- p_yes_laplace
print(p_yes_laplace)
print(p_no_laplace)
#1d
total = 0;
for k in trainData.keys():
    attSet=set()
    for v in trainData[k]:
        attSet.add(v)
    print("P( "+k + " | Y = Yes): "+  str(len(attSet)) + " parameters")
    print("P( "+k + " | Y = No): "+  str(len(attSet))+ " parameters")
    total+= (2*len(attSet))
print("total parameters:"+ str(total))
