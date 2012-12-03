#!/usr/bin/env python
import sys
import os
import ujson
import fileinput
import ast
import classifier


if __name__=="__main__":
    vals = filterFeatures(fileinput.input())


