import csv,sys,random

if len(sys.argv) !=5:
    print("invalid number of arguments : correct usage \"python kmeans.py yelp3.csv K {1-5} {1,2,no}\"")
    exit()
def setData(filename):
    attributes=['latitude','longitude','reviewCount','checkins']
    trainingDataFilename =open(filename)
    reader = csv.reader(trainingDataFilename)
    headers = reader.next()
    data = {}
    for h in headers:
        data[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            data[h].append(v)
    selectData={}
    for h in attributes:
        selectData[h] = data[h]
    points=[]
    for i in range(len(selectData['latitude'])):
        point=[]
        for h in attributes:
            point.append(float(selectData[h][i]))
        points.append(point)
    return points
def distance(point1, point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2+(point1[3]-point2[3])**2)**1/2
def closest_centroid(data,centroids):
    minIndexes=[]
    for point in data:
        means = []
        for centroid in centroids:
            means.append(distance(point,centroid))
        minIndexes.append(means.index(min(means)))
    return minIndexes
def printCentroids(centroids):
    for i,centroid in enumerate(centroids):
        print "centroid"+str(i+1)+"="+str(centroid)
    print
data = setData(sys.argv[1])
rows = len(data)
kValue = int(sys.argv[2])
if kValue > rows:
    print "K value is greater than number of rows"
    exit()
clusteringOption=int(sys.argv[3])
plotOption=sys.argv[4]
centroids=[]
randomNums = random.sample(range(0,rows),kValue)
# get random initial centroids
for i in randomNums:
    centroids.append(data[i])
printCentroids(centroids)
#get array of index of closest centroid for each point
while True:
    closestCentroid = closest_centroid(data,centroids)
    clusters=[]
    for k in range(len(centroids)):
        points=[]
        for i,c in enumerate(closestCentroid):
            if c == k:
                points.append(data[i])
        clusters.append(points)
    #calculate new centroids
    newCentroids=[]
    for cluster in clusters:
        newCentroid=[]
        for i in range(4):
            subval=0
            for point in cluster:
                subval+=point[i]
            newCentroid.append(subval/len(cluster))
        newCentroids.append(newCentroid)
    same = True
    for newCentroid,oldCentroid in zip(newCentroids,centroids):
        for x in range(len(newCentroid)):
            if newCentroid[x]!=oldCentroid[x]:
                same = False
                break
        if same == False:
            break
    if same == False:
        centroids= newCentroids
    else:
        printCentroids(newCentroids)
        break
