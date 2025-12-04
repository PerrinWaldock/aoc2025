import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        lines = f.readlines()
    arr = np.array([list(l.strip()) for l in lines])
    removedRolls = []
    
    while True:
        rolls = np.argwhere(arr == "@")
        moveableRolls = []
        for roll in rolls:
            if countAdjacentRolls(roll, arr) < 4+1:  
                moveableRolls.append(roll)
        for roll in moveableRolls:
            removedRolls.append(roll)
            arr[*roll] = "x"
        if len(moveableRolls) == 0:
            break 
    print(len(removedRolls))

def countAdjacentRolls(loc, arr):
    tl = np.maximum(loc - [1,1], [0,0])
    br = np.minimum(loc + [1,1], np.array(arr.shape) - [1,1])
    subarr = arr[tl[0]:(br[0]+1),tl[1]:(br[1]+1)]
    return len(np.argwhere(subarr == "@"))

if __name__ == "__main__":
    main()