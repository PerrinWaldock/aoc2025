import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    freshRanges = []
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        for line in f:
            if line.strip() == "":
                break
            else:
                freshRanges.append(tuple(map(int, line.strip().split("-"))))
    orderedRanges = sorted(freshRanges, key=lambda x: x[0])
    mergedPairs = []
    for pair in orderedRanges:
        if len(mergedPairs) == 0:
            mergedPairs.append(pair)
        else:
            lastPair = mergedPairs[-1]
            if pair[0] <= lastPair[1] + 1:
                mergedPairs[-1] = (lastPair[0], max(lastPair[1], pair[1]))
            else:
                mergedPairs.append(pair)
    ingredientCount = sum(map(lambda x: x[1]-x[0]+1, mergedPairs))
    print(ingredientCount)

if __name__ == "__main__":
    main()