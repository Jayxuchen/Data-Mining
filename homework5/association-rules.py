import csv,sys,random,math
import numpy as np

def setData(filename):
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
            if len(v) <1:
                data[h].append('BLANK')
                sets[h].add('BLANK')
            else:
                data[h].append(v)
                sets[h].add(v)
    for k in matrix.keys():
        for n in sets[k]:
            matrix[k][n]=[]
    # matrix['rating']['4'][]
    for x in range(9337):
        for k in matrix.keys():
            for n in matrix[k].keys():
                if data[k][x] == n:
                    matrix[k][n].append(True)
                else:
                    matrix[k][n].append(False)
    # print matrix['stars']['4']
    return matrix

if len(sys.argv) !=4:
    print("invalid number of arguments : correct usage \"python association-rules.py yelp4.csv minsup minconf\"")
    exit()
filename =  sys.argv[1]
minsup = float(sys.argv[2])
minconf = float(sys.argv[3])
matrix = setData(filename)
# setData()
