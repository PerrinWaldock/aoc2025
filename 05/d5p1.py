import os
import numpy as np
from functools import cache

filename = "sample.txt"
filename = "input.txt"

def main():
    parsingIngredients = False
    freshRanges = []
    ingredients = []
    freshIngredients = []
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        for line in f:
            if line.strip() == "":
                parsingIngredients = True
                continue
            if parsingIngredients:
                ingredients.append(int(line.strip()))
            else:
                freshRanges.append(tuple(map(int, line.strip().split("-"))))
    for ingredient in ingredients:
        if isFresh(ingredient, freshRanges):
            freshIngredients.append(ingredient)
    print(len(freshIngredients))

def isFresh(value, freshRanges):
    for fr in freshRanges:
        if value >= fr[0] and value <= fr[1]:
            return True
    return False

if __name__ == "__main__":
    main()