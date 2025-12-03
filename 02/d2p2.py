import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

with open(os.path.join(os.path.dirname(__file__), filename)) as f:
    lines = "".join(f.readlines())
    groups = lines.split(",")
    ranges = [[int(y) for y in g.split("-")] for g in groups]

def isInvalid(n):
    stringed = str(n)
    numlength = len(stringed)
    comboLengths = primeFactors(numlength)
    for comboLength in comboLengths:
        if isRepeatedCombo(stringed, comboLength):
            return True
    return False

def isRepeatedCombo(stringed, comboLength):
    chunkedStrings = list(chunkString(stringed, comboLength))
    chunkedStringsSet = set(chunkedStrings)
    return len(chunkedStrings) != 1 and len(chunkedStringsSet) == 1

def chunkString(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

@cache
def primeFactors(n):
    factors = [1]
    for i in range(2, (n//2) + 1):
        if n % i == 0:
            factors.append(i)
    return set(sorted(factors))

invalidIds = []
for pair in ranges:
    n = pair[0]
    while n <= pair[1]:
        if isInvalid(n):
            print(n)
            invalidIds.append(n)
        n += 1
print(sum(invalidIds))
    