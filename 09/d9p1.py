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
    points = [tuple(map(int, line.split(","))) for line in lines]
    areas = []
    for a in points:
        for b in points:
            areas.append(area(a, b))
    print(max(areas))

def area(a, b):
    return abs((a[0] - b[0] + 1) * (a[1] - b[1] + 1))

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()