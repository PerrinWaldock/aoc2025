import os
import numpy as np
from functools import cache

filenames = ["sample.txt", "input.txt"]

def main():
    for filename in filenames:
        print(filename)
        lines = getLines(filename)
        mainFunction(lines)

def mainFunction(lines):
    connections = dict()
    for line in lines:
        key, rest = line.split(":")
        nodes = map(str.strip, rest.strip().split(" "))
        connections[key] = tuple(nodes)

    @cache
    def countPaths(node):
        if node == "out":
            return 1
        else:
            return sum(countPaths(n) for n in connections[node])
    totalPaths = countPaths("you")
    print(totalPaths)
        

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()