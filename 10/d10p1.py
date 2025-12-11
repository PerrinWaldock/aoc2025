import os
from platform import machine
import numpy as np
from functools import cache
from collections import namedtuple

Machine = namedtuple("Machine", ["lightNumber", "buttonwirings", "joltages"])

filenames = ["sample.txt", "input.txt"]

def main():
    for filename in filenames:
        print(filename)
        lines = getLines(filename)
        mainFunction(lines)

def mainFunction(lines):
    machines = map(getMachine, lines)
    buttonCounts = []
    for m in machines:
        buttons = bruteForce(m)
        print(m)
        print(buttons)
        buttonCounts.append(len(buttons))
    print(sum(buttonCounts))

def bruteForce(machine):
    for pressedButtons in getButtonCombos(len(machine.buttonwirings)):
        lights = getLights(machine.buttonwirings, pressedButtons)
        if lights == machine.lightNumber:
            return pressedButtons
    pass

@cache
def getButtonCombos(n):
    sets = set()
    formatString = "{0:0"+str(n) + "b}"
    for buttonComboNumber in range(1, 2**n):
        pressedButtons = tuple([i for i, bit in enumerate(reversed(formatString.format(buttonComboNumber))) if bit == '1'])
        sets.add(pressedButtons)
    sortedSets = sorted(sets, key=lambda x: len(x))
    return sortedSets

def getMachine(line):
    buttonWirings = []
    for segment in line.split():
        if segment[0] == "[":
            lightStates = tuple([1 if c == "#" else 0 for c in reversed(segment[1:-1])])
            lightNumber = int(''.join(map(str, lightStates)), 2)
        elif segment[0] == "{":
            joltages = tuple(map(int, segment[1:-1].split(",")))
        else:
            buttonWire = tuple(map(int, segment[1:-1].split(",")))
            buttonNumber = 0
            for ind in buttonWire:
                buttonNumber |= 1 << ind
            buttonWirings.append(buttonNumber)
            
    machine = Machine(lightNumber=lightNumber, buttonwirings=buttonWirings, joltages=joltages)
    return machine

def getLights(buttonWirings, pressedButtons):
    lightNumber = 0
    for button in pressedButtons:
        lightNumber ^= buttonWirings[button]
    return lightNumber

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()