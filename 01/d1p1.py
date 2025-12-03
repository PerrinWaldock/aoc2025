import os

#filename = "test.txt"
filename = "input.txt"

value = 50
maxvalue = 100
zerocount = 0
with open(os.path.join(os.path.dirname(__file__), filename)) as f:
    for line in f:
        if line[0] == "L":
            value -= int(line[1:])
        elif line[0] == "R":
            value += int(line[1:])
        if value % maxvalue == 0:
            zerocount += 1
print(zerocount)