import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    joltages = []
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        for line in f:
            j = getJoltage(np.array(list(line.strip())))
            joltages.append(j)
    print(sum(joltages))

def getJoltage(linelist):
    maxDigit = max(linelist[:-1])
    ind = np.argwhere(linelist == maxDigit)[0][0]
    secondDigit = max(linelist[ind+1:])
    return int(maxDigit + secondDigit)

if __name__ == "__main__":
    main()