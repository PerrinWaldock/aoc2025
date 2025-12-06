import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    lines = getLines()
    maxwidth = max([len(line) for line in lines])
    lines = [line + " "*(maxwidth - len(line)) for line in lines]
    arr = np.array([list(l) for l in lines])
    arrt = np.transpose(arr)
    groups = []
    group = []
    for line in arrt:
        if set(line) == set(" "):
            groups.append(group)
            group = []
        else:
            group.append(line)
    groups.append(group)
    
    numbers = list(map(createGroup, groups))
    answers = map(computeGroup, numbers)
    print(sum(answers))

def createGroup(lines):
    numbers = []
    operator = lines[0][-1]
    for line in reversed(lines):
        line = "".join(line).replace(operator, " ")
        numbers.append(line.strip())
    numbers.append(operator)
    return numbers
    
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
        return [line.replace("\n", "") for line in f.readlines()]
    
if __name__ == "__main__":
    main()