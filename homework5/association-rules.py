import csv,sys,random,math, collections
import numpy as np
from  itertools import chain,combinations
binaryAtts=['delivery','waiterService','caters']
dataSize = 9337
def setData(filename):
    global binaryAtts
    trainingDataFilename =open(filename)
    reader = csv.reader(trainingDataFilename)
    headers = reader.next()
    data = {}
    sets= {}
    matrix = {}
    for h in headers:
        data[h] = []
        matrix[h] = {}
        sets[h] = set()
    for row in reader:
        for h, v in zip(headers, row):
            data[h].append(v)
            sets[h].add(v)
    for k in matrix.keys():
        if k in binaryAtts:
            matrix[k] = []
        else:
            for n in sets[k]:
                matrix[k][n]=[]
    # matrix['rating']['4'][]
    for x in range(9337):
        for k in matrix.keys():
            if k in binaryAtts:
                if data[k][x] == 'TRUE':
                    matrix[k].append(True)
                else:
                    matrix[k].append(False)
            else:
                for n in matrix[k].keys():
                    if data[k][x] == n:
                        matrix[k][n].append(True)
                    else:
                        matrix[k][n].append(False)
    # print matrix['stars']['4']
    return matrix
def getColumns(matrix):
    count = 0
    for k in matrix.keys():
        if type(matrix[k]) is dict:
            for n in matrix[k].keys():
                count+=1
        else:
            count+=1
    return count
def computeApriori(data, minsup, minconf):
    global dataSize
    itemset = frequentItemsetGeneration(data,minsup)
    rules = ruleGeneration(itemset,minconf)
    return rules
def ruleGeneration(itemset, minconf):
    global dataSize
    return itemset
def generateInitialCandidates(matrix):
    global dataSize
    itemset={}
    for k in matrix.keys():
        if type(matrix[k]) is dict:
            for n in matrix[k].keys():
                count = 0
                for x in matrix[k][n]:
                    if x == True:
                        count+=1
                key = k+"$"+ n
                itemset[key] = count/float(dataSize)
        else:
            count = 0
            for x in matrix[k]:
                if x == True:
                    count+=1
            key = k+"$"
            itemset[key] = count/float(dataSize)
    return itemset
def candidatesItemsetGeneration(frequentItemsets,minsup):
    k = len(frequentItemsets.keys()[0].strip().split(" ")) + 1
    tuples = list(combinations(iter(frequentItemsets.keys()),2))
    nextItemset=[]
    # print tuples
    # print
    for t in tuples:
        if t[0] != t[1]:
            p = t[0].strip().split(" ")
            q = t[1].strip().split(" ")
            m = k-1
            for i in range(m):
                if i < (m-1):
                    if p[i] != q[i]:
                        break
                else:
                    if p[i] < q[i]:
                        p.append(q[i])
                        nextItemset.append(p)
    for i in nextItemset: print i
    print
    #pruning
    prunedItemset=[]
    # print len(nextItemset)
    for c in nextItemset:
        # print c
        subsets = list(combinations(c,k-1))
        isValid = True
        for ar in subsets:
            string =""
            for s in ar:
                string+= s +" "
                string = string.strip()
            # print string
            if string not in frequentItemsets.keys():
                isValid = False
        if isValid:
            prunedItemset.append(c)
    # print prunedItemset
    # for i in prunedItemset: print i
    nextItemset = calculateSupport(prunedItemset)
    return nextItemset

def calculateSupport(keyList):
    global binaryAtts
    global dataSize
    global matrix
    itemSet={}
    for subset in keyList:
        count = 0
        newKey=""
        for item in subset:
            newKey+=item+" "
        for i in range(dataSize):
            isValid = True
            for item in subset:
                arr = item.split("$")
                if arr[0] in binaryAtts:
                    # print arr[0]+":"+str(matrix[arr[0]][i])
                    if matrix[arr[0]][i] != True:
                        isValid = False
                        break
                else:
                    # print item+":"+str(matrix[arr[0]][arr[1]][i])
                    if matrix[arr[0]][arr[1]][i] != True:
                        isValid = False
                        break
            if isValid:
                count+=1
                # print str(subset) + str(i)
        itemSet[newKey.strip()] = count/float(dataSize)
    return itemSet
def pruneCandidates(candidates,minsup):
    frequentItems = {}
    for x in candidates.keys():
        if candidates[x] >= minsup:
            frequentItems[x]= candidates[x]
    sortedFrequentItems = collections.OrderedDict(sorted(frequentItems.items()))
    return sortedFrequentItems
def frequentItemsetGeneration(matrix, minsup):
    global dataSize
    i = 0
    candidates=[]
    candidates.append(generateInitialCandidates(matrix))
    frequentItems=[]
    frequentItems.append(pruneCandidates(candidates[i],minsup))
    # print frequentItems[i]
    # print
    while len(candidates[i]) != 0:
        candidates.append(candidatesItemsetGeneration(frequentItems[i],minsup))
        # print candidates[i+1]
        # print
        frequentItems.append(pruneCandidates(candidates[i+1],minsup))
        # print frequentItems[i+1]
        # print
        i+=1
    return frequentItems[i]
if len(sys.argv) !=4:
    print("invalid number of arguments : correct usage \"python association-rules.py yelp4.csv minsup minconf\"")
    exit()
filename =  sys.argv[1]
minsup = float(sys.argv[2])
minconf = float(sys.argv[3])
matrix = setData(filename)
associationRules=computeApriori(matrix,minsup,minconf)
# print
# for x in associationRules.items():
#     print x
