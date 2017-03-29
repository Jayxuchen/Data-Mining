import csv,sys,random,math
import matplotlib.pyplot as plt
import numpy as np
# plt.plot([1,2,3,4])
# plt.ylabel('some numbers')
# plt.show()
# exit()
manhattan= False
if len(sys.argv) !=5:
    print("invalid number of arguments : correct usage \"python kmeans.py yelp3.csv K {1-5} {1,2,no}\"")
    exit()
def setData(filename,clusteringOption):
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

    #clustering option
    if clusteringOption== 2:
        for i in range(len(data['reviewCount'])):
                data['reviewCount'][i] = math.log(float(data['reviewCount'][i]),2)
                data['checkins'][i] = math.log(float(data['checkins'][i]),2)
    elif clusteringOption==3:
        for attribute in attributes:
            mean= np.mean(map(float,data[attribute])).item()
            std = np.std(map(float,data[attribute])).item()
            for i in range(len(data[attribute])):
                data[attribute][i]= (float(data[attribute][i]) - mean)/ std
    elif clusteringOption==4:
        global manhattan
        manhattan=True
    # print manhattan
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
def distance(c1, c2):
    global manhattan
    if manhattan:
        # print 'using manhattan'
        return abs(c1[0]-c2[0])+abs(c1[1]-c2[1])+abs(c1[2]-c2[2])+abs(c1[3]-c2[3])
    else:
        return ((c1[0]-c2[0])**2+(c1[1]-c2[1])**2+(c1[2]-c2[2])**2+(c1[3]-c2[3])**2)**(1/2.0)
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
def printSSE(clusters,centroids):
    tot = 0
    for centroid,cluster in zip(centroids,clusters):
        for point in cluster:
            tot+=(distance(point,centroid)**2)
    print "WC-SSE="+str(tot)
def runKMeans(data,rows,kValue):
    centroids=[]
    randomNums = random.sample(range(0,rows),kValue)
    # get random initial centroids
    for i in randomNums:
        centroids.append(data[i])
    # printCentroids(centroids)
    #get array of index of closest centroid for each point
    cycles=0
    while True:
        cycles+=1
        closestCentroid = closest_centroid(data,centroids)
        clusters=[]
        for k in range(len(centroids)):
            points=[]
            for i,c in enumerate(closestCentroid):
                if c == k:
                    points.append(data[i])
            clusters.append(points)
        for i in range(len(clusters)):
            if len(clusters[i]) == 0:
                # print clusters[i]
                clusters[i].append(centroids[i])
                # print "added centroid"+str(centroids[i])
                # print clusters[i]

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
            # print "Cycles="+str(cycles)
            printSSE(clusters,centroids)
            printCentroids(newCentroids)
            break
#begin
clusteringOption=int(sys.argv[3])
data = setData(sys.argv[1],clusteringOption)
# print manhattan
rows = len(data)
kValue = int(sys.argv[2])
if kValue > rows:
    print "K value is greater than number of rows"
    exit()
plotOption=sys.argv[4]
if clusteringOption in [1,2,3,4]:
    runKMeans(data,rows,kValue)
elif clusteringOption == 5:
    newData=[]
    randomNums=random.sample(range(0,rows),int(math.floor(.03*rows)))
    for i in randomNums:
        newData.append(data[i])
    kVals=[3,6,9,12,24,48]
    for k in kVals:
        print "K="+str(k)
        for i in range(5):
            print "trial="+str(i+1)
            runKMeans(newData,len(newData),k)
        print
