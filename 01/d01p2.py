import os
import numpy as np

#filename = "test.txt"
filename = "input.txt"

value = 50
maxvalue = 100
zerocount = 0
with open(os.path.join(os.path.dirname(__file__), filename)) as f:
    for line in f:
        if line[0] == "L":
            delta = -int(line[1:])
        elif line[0] == "R":
            delta = int(line[1:])
        newvalue = value + delta
        if newvalue >= maxvalue:
            crossings = newvalue // maxvalue
        elif newvalue <= 0:
            offset = 1 if value != 0 else 0
            crossings = (-1*newvalue // maxvalue) + offset
        else:
            crossings = 0
        value = newvalue % maxvalue
        zerocount += crossings
print(zerocount)