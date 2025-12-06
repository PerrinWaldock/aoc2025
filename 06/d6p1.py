import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    lines = getLines()
    groups = []
    for line in lines:
        groups.append(splitNoneWhitespace(line))
    groups = np.transpose(groups)
    answers = map(computeGroup, groups)
    print(sum(answers))
    
def computeGroup(group):
    operator = group[-1]
    if operator == "*":
        return np.prod([int(x) for x in group[:-1]])
    elif operator == "+":
        return np.sum([int(x) for x in group[:-1]])

def splitNoneWhitespace(line):
    return [x for x in line.split(" ") if x != ""]

def getLines():
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.strip() for line in f.readlines()]
    
if __name__ == "__main__":
    main()