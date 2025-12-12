import os
import numpy as np
from functools import cache
from collections import namedtuple
"""
# is occupied, . is not

notes
    all shapes fit in a 3x3 grid. This may be important
    first impression: recursive algorithm with input shape the returns all shapes that fit in the space
    need to think about how best to represent shapes:
        ascii characters?
        set of occupied coordinates?
    how to represent regions:
        collection of unoccupied coordinates?
        straight ascii grid?
    how to determine if something can fit
        see if shape coordinates exist in region. If not, increment coordinates and retry?
            note: regions may need to track their "dead zone" somehow...
"""

Tree = namedtuple("Tree", ["dimensions", "numbers"])
filenames = ["sample.txt", "input.txt"]

trees = []
shapes = []
shapePermutations = []

def main():
    for filename in filenames:
        print(filename)
        lines = getLines(filename)
        mainFunction(lines)

def mainFunction(lines):
    global shapes, trees, shapePermutations
    shapes, trees = getInput(lines)
    shapePermutations = [getShapePermutations(s) for s in shapes]
        
    goodTrees = 0
    for tree in trees:
        if (tree.dimensions[0]//3)*(tree.dimensions[1]//3) >= sum(tree.numbers):
            goodTrees += 1
    print(goodTrees)
    

def getInput(lines):
    shapes = []
    trees = []
    parsingShapes = True
    currentShapeLines = []
    for line in lines:
        if line == "":
            if parsingShapes:
                shapes.append(toArray(currentShapeLines))
                currentShapeLines = []
            parsingShapes = False
        else:
            if "x" in line:
                parsingShapes = False
            else:
                parsingShapes = True
                
            if parsingShapes and ":" not in line:
                currentShapeLines.append(line)
            elif not parsingShapes:
                dimensions, numbers = line.split(":")
                dimensions = tuple(int(d) for d in dimensions.split("x"))
                numbers = tuple(int(n.strip()) for n in numbers.split(" ") if n != "")
                tree = Tree(dimensions, numbers)
                trees.append(tree)
    return shapes, trees

def rotate(shape, rotations):
    for _ in range(rotations):
        shape = np.rot90(shape)
    return shape

def mirrorx(shape):
    return np.flip(shape, axis=1)
 
def mirrory(shape):
    return np.flip(shape, axis=0)

def getShapePermutations(shape):
    allShapes = []
    mirroredShape = mirrorx(shape)
    for rotations in range(4):
        allShapes.append(rotate(shape, rotations))
        allShapes.append(rotate(mirroredShape, rotations))
    uniqueShapes = set([arrToTuple(s) for s in allShapes])
    return [tupleToArr(s) for s in uniqueShapes]

def arrToTuple(arr):
    return tuple(tuple(row) for row in arr)

def tupleToArr(t):
    return np.array(t)

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()