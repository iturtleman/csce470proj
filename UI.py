#!/usr/bin/env python
import sys
import os
import ujson
import fileinput
import ast

def filterFeatures(lines):
    avg=0.0
    count=0
    vals = {}
    for line in lines:
        vals = ujson.loads(line)
        for key,val in vals.iteritems():
            avg += val
            count +=1
    avg = avg/count
    for key,val in vals.items():
        if val < avg:
            del vals[key]
    return vals

if __name__=="__main__":
    vals = filterFeatures(fileinput.input())


