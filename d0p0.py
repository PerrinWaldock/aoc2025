import os
import numpy as np
from functools import cache

filename = "sample.txt"
# filename = "input.txt"

def main():
    lines = getLines()



def getLines():
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.strip() for line in f.readlines()]
    
if __name__ == "__main__":
    main()