import os
import numpy as np

#filename = "sample.txt"
filename = "input.txt"

with open(os.path.join(os.path.dirname(__file__), filename)) as f:
    lines = "".join(f.readlines())
    groups = lines.split(",")
    ranges = [[int(y) for y in g.split("-")] for g in groups]

def isInvalid(n):
    stringed = str(n)
    if len(stringed)%2 == 1:
        return False
    elif stringed[:len(stringed)//2] == stringed[len(stringed)//2:]:
        return True
    else:
        return False

invalidIds = []
for pair in ranges:
    n = pair[0]
    while n <= pair[1]:
        if isInvalid(n):
            invalidIds.append(n)
        if len(str(n))%2 == 1:
            n = int("1" + "0"*(len(str(n))))
        else:
            n += 1
print(sum(invalidIds))
    