import os
import numpy as np
from functools import cache
from collections import namedtuple

PathCount = namedtuple("PathCount", ["neither", "fft", "dac", "both"])

filenames = ["sample2.txt", "input.txt"]

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
            return PathCount(1, 0, 0, 0)
        else:
            thisPathCount = PathCount(0, 0, 0, 0)
            for n in connections[node]:
                subpathcount = countPaths(n)
                thisPathCount = PathCount(
                    thisPathCount.neither + subpathcount.neither,
                    thisPathCount.fft + subpathcount.fft,
                    thisPathCount.dac + subpathcount.dac,
                    thisPathCount.both + subpathcount.both,
                )
            if node == "fft":
                thisPathCount = PathCount(
                    0,
                    thisPathCount.neither + thisPathCount.fft,
                    0,
                    thisPathCount.dac + thisPathCount.both,
                )
            elif node == "dac":
                thisPathCount = PathCount(
                    0,
                    0,
                    thisPathCount.neither + thisPathCount.dac,
                    thisPathCount.fft + thisPathCount.both
                )
            
            return thisPathCount
    totalPaths = countPaths("svr")
    print(totalPaths.both)        

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()