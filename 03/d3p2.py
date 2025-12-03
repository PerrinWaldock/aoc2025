import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    joltages = []
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        for line in f:
            j = int(getJoltage(np.array(list(line.strip())), 12))
            joltages.append(j)
            print(j)
    print(sum(joltages))

def getJoltage(linelist, n):
    if n == 1:
        return max(linelist)
    elif len(linelist) == n:
        return "".join(linelist)
    else:
        maxDigit = max(linelist[:-(n-1)])
        ind = np.argwhere(linelist == maxDigit)[0][0]
        return maxDigit + str(getJoltage(linelist[ind+1:], n-1))

if __name__ == "__main__":
    main()