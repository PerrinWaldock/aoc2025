import os
import numpy as np
from functools import cache

filenames = ["sample.txt", "input.txt"]

def main():
    for filename in filenames:
        lines = getLines(filename)
        mainFunction(lines)

def mainFunction(lines):
    pass

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()