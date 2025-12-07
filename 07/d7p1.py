import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    lines = getLines()
    arr = np.array([list(line) for line in lines])
    start = np.argwhere(arr[0] == "S")[0][0]
    entries = set([start])
    beamsplits = 0
    for line in lines:
        entries, newsplits = propagate(line, entries)
        beamsplits += newsplits
    print(beamsplits)

def propagate(line, entries):
    exits = set()
    splits = 0
    for entry in entries:
        if line[entry] == "." or line[entry] == "S":
            exits.add(entry)
        elif line[entry] == "^":
            splits += 1
            if entry + 1 < len(line):
                exits.add(entry + 1)
            if entry - 1 >= 0:
                exits.add(entry - 1)
    return exits, splits
                
def getLines():
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.strip() for line in f.readlines()]
    
if __name__ == "__main__":
    main()