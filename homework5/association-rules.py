import csv,sys,random,math
import numpy as np

def setData(filename):
    trainingDataFilename =open(filename)
    reader = csv.reader(trainingDataFilename)
    headers = reader.next()
    data = {}
    sets {}
    for h in headers:
        data[h] = []
        sets[h] = set()
    for row in reader:
        for h, v in zip(headers, row):
            if len(v) <1:
                data[h].append('BLANK')
                sets[h].add('BLANK')
            else:
                data[h].append(v)
                sets[h].add(v)
    return data

if len(sys.argv) !=5:
    print("invalid number of arguments : correct usage \"python association-rules.py yelp4.csv minsup minconf\"")
    exit()
