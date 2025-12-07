import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    lines = getLines()
    arr = np.array([list(line) for line in lines])

    @cache
    def countTimelines(row, position):
        if row > len(arr) - 1:
            return 1
        exits = propagate(arr[row], position)
        timelines = 0
        for exit in exits:
            timelines += countTimelines(row + 1, exit)
        return timelines
    
    start = np.argwhere(arr[0] == "S")[0][0]
    timelines = countTimelines(0, start)
    print(timelines)

def propagate(line, entry):
    exits = []
    splits = 0
    if line[entry] == "." or line[entry] == "S":
        exits.append(entry)
    elif line[entry] == "^":
        splits += 1
        if entry + 1 < len(line):
            exits.append(entry + 1)
        if entry - 1 >= 0:
            exits.append(entry - 1)
    return exits
                
def getLines():
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.strip() for line in f.readlines()]
    
if __name__ == "__main__":
    main()