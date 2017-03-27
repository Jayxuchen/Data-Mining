import csv,sys

if len(sys.argv) !=5:
    print("invalid number of arguments : correct usage \"python kmeans.py yelp3.csv K {1-5} {1,2,no}\"")
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
data = setData(sys.argv[1])
kValue = int(sys.argv[2])
clusteringOption=int(sys.argv[3])
plotOption=sys.argv[4]
