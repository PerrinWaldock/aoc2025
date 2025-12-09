import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from functools import cache
from tqdm import tqdm

filenames = ["sample.txt", "input.txt"]

def main():
    for filename in filenames[1:2]:
        print(filename)
        lines = getLines(filename)
        mainFunction(lines)
    plt.show()

def mainFunction(lines):
    points = [tuple(map(int, line.split(","))) for line in lines]
    plt.figure()
    plt.plot(*zip(*points), color="green")
    plt.scatter(*zip(*points), color="red", s=2, marker="s")
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal', adjustable='box')
    
    areasByPoints = {}
    for a in points:
        for b in points:
            if a != b:
                area = calculateArea(a, b)
                if not (b,a) in areasByPoints:
                    areasByPoints[(a,b)] = area
    sortedKeys = sorted(areasByPoints, key=areasByPoints.get, reverse=True)
    
    points.append(points[0])
    for (a, b) in tqdm(sortedKeys):
        (tl, br) = tlbr(a, b)
        area = areasByPoints[(a,b)]
        isAllColoured = True
        for point, nextpoint in zip(points, points[1:]):
            if isInsideRectangleInterior(point, tl, br):
                isAllColoured = False
                break
            if crossesRectangle(tl, br, point, nextpoint):
                isAllColoured = False
                break
        if isAllColoured:
            break
    plt.gca().add_patch(Rectangle(tl, br[0]-tl[0], br[1]-tl[1],
             edgecolor = 'blue',
             facecolor = 'blue',
             fill=True,
             alpha=0.2,
             lw=0))
    print(area)

def isInsideRectangleInterior(p, tl, br):
    return tl[0] < p[0] < br[0] and tl[1] < p[1] < br[1]

def isOnRectanglePerimeter(p, tl, br):
    return tl[0] <= p[0] <= br[0] and tl[1] <= p[1] <= br[1] and not isInsideRectangleInterior(p, tl, br)

def getPointsBetween(a, b):
    if a[0] == b[0]:
        for y in range(min(a[1], b[1]), max(a[1], b[1])):
            yield (a[0], y)
    elif a[1] == b[1]:
        for x in range(min(a[0], b[0]), max(a[0], b[0])):
            yield (x, a[1])

def tlbr(a, b):
    tl = (min(a[0], b[0]), min(a[1], b[1]))
    br = (max(a[0], b[0]), max(a[1], b[1]))
    return (tl, br)

def trbl(a, b):
    tr = (max(a[0], b[0]), min(a[1], b[1]))
    bl = (min(a[0], b[0]), max(a[1], b[1]))
    return (tr, bl)

def crossesRectangle(tl, br, c, d):
    (tl2, br2) = tlbr(c, d)
    if tl2[0] == br2[0]:
        x = tl2[0]
        if tl[0] < x < br[0] and tl2[1] <= tl[1] and br[1] <= br2[1]:
            return True
        else:
            return False
    elif tl2[1] == br2[1]:
        y = tl2[1]
        if tl[1] < y < br[1] and tl2[0] <= tl[0] and br[0] <= br2[0]:
            return True
        else: 
            return False
    else:
        raise Exception("Not orthogonal line")
    
def calculateArea(a, b):
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

def lineLength(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + 1

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()