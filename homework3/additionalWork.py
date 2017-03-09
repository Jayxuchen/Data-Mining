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
yelpData = setData('yelp2.csv')
print(len(yelpData['goodForGroups']))
#1c
count = 0
for v in yelpData['goodForGroups']:
     if v=='1':count+=1
p_yes=str(count)+ "/" +str(len(yelpData['goodForGroups']))
p_no= str(len(yelpData['goodForGroups'])-count) + "/" + str(len(yelpData['goodForGroups']))
print(p_yes)
print(p_no)
p_yes_laplace=(count+1)/(float(len(yelpData['goodForGroups']))+2)
p_no_laplace =1- p_yes_laplace
print(p_yes_laplace)
print(p_no_laplace)
#1d
total = 0;
for k in yelpData.keys():
    if k == classLabel:
        continue
    attSet=set()
    for v in yelpData[k]:
        attSet.add(v)
    print("P( "+k + " | Y = Yes): "+  str(len(attSet)) + " parameters")
    print("P( "+k + " | Y = No): "+  str(len(attSet))+ " parameters")
    total+= (2*len(attSet))
print("total parameters:"+ str(total))
#1e
