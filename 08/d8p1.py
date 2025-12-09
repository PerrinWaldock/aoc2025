import os
import numpy as np
from functools import cache

filenames = ["sample.txt", "input.txt"]

numberOfConnections = 10

def main():
    for filename in filenames:
        global numberOfConnections
        if "sample" in filename:
            numberOfConnections = 10
        else:
            numberOfConnections = 1000    
        lines = getLines(filename)
        print(filename)
        mainFunction(lines)

def mainFunction(lines):
    boxes = [tuple(map(int, line.split(","))) for line in lines]
    circuits = [set([box]) for box in boxes]
    closestOther = findClosestOthers(boxes)
    for _ in range(numberOfConnections):
        closestDistance = {b1: distance(b1, bs[0]) for b1, bs in closestOther.items()}
        closest1 = min(closestDistance, key=closestDistance.get)
        closest2 = closestOther[closest1][0]
        closestOther[closest1].remove(closest2)
        closestOther[closest2].remove(closest1)
        relevantCircuits = [c for c in circuits if closest1 in c or closest2 in c]
        for c in relevantCircuits[1:]:
            relevantCircuits[0].update(c)
            circuits.remove(c)
    circuitSizes = list(reversed(sorted([len(c) for c in circuits])))
    print(np.prod(circuitSizes[:3]))
    
def findClosestOthers(boxes):
    return {box: orderByClosestTo(box, boxes) for box in boxes}

def orderByClosestTo(box, otherBoxes):
    validBoxes = [b for b in otherBoxes if box != b]
    closestCircuit = sorted(validBoxes, key=lambda b: distance(box, b))
    return closestCircuit

def distance(b1, b2):
    return sum(abs(a - b)**2 for a, b in zip(b1, b2))

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()