import os
from platform import machine
import numpy as np
from functools import cache
from collections import namedtuple
import sympy as sp
from sympy import Matrix
from sympy import solve_linear_system
from tqdm import tqdm
from multiprocessing import Pool
import pulp as pp

Machine = namedtuple("Machine", ["lightNumber", "buttonwirings", "joltages"])

filenames = ["sample.txt", "input.txt"]

"""
possible solution:
    enumerate all solutions, just find the lowest
    enumerating solutions:
        from the smallest joltage to the largest, find all combinations of button presses that can produce it, look for set intersections?
            not viable, millions of combinations

invalid machines:
    52
        pulp gives 2.0, 16.0, 18.0, 20.0, 13.0, 1.0, 19.0, 1.0, 10.0
        (5*b_8/3 - 44/3, 
        26 - b_8, 
        74/3 - 2*b_8/3, 
        80/3 - 2*b_8/3, 
        2*b_8/3 + 19/3, 
        b_8/3 - 7/3, 
        19, 
        13/3 - b_8/3, 
        b_8)
            1: b8 == (3n + 44)/5 -> n is 2, 7, 12, 17, 22, 27 -> 1, 4, 7, 10, 13, 16, 19
            2: b8 <= 26
            3: b8 == (3/2)n - 37 -> n >= 25, n is even, and b8 <= 37 -> 2, 5, 8, 11, ...
            4: b8 == (3/2)n - 40 -> n is even .... 2, 5, 8, 11
            5:  .... 1, 4, 7, 10, ...
            6: 1, 4, 7, 10, ....
            7: any
            8: 1, 4, 7, 10, ...
        confirmed invalid -- is something wrong with the parser?
            
            b_8 must follow 1 + 3n
            
        
    54
    59
    62
    76
    135
    181
    
"""

def main():
    for filename in filenames:
        print(filename)
        lines = getLines(filename)
        mainFunction(lines)

def mainFunction(lines):
    machines = list(map(getMachine, lines))
    buttonPressCounts = []
    for ind, m in enumerate(tqdm(machines)):
        tqdm.write(f"{ind}: {m}")
        presses = solveWithPulp(m) #solveWithSympy(m)
        pressSum = sum(presses)
        tqdm.write(str(presses))
        tqdm.write(str(pressSum))
        if isAnswerValid(presses):
            buttonPressCounts.append(pressSum)
        else:
            tqdm.write(f"MACHINE {ind} HAS NO VALID SOLUTION!!!")
    print("Solution:")
    print(sum(buttonPressCounts))

def solveWithMatrices(machine: Machine):
    #gives floats and wrong answer
    pressMatrix = np.array(machine.buttonwirings).T
    leftInverse = np.linalg.pinv(pressMatrix)
    tqdm.write(str(leftInverse))
    presses = np.matmul(leftInverse, np.array(machine.joltages))
    tqdm.write(str(presses))
    tqdm.write(str(getJoltagesFromPressMatrix(pressMatrix, presses)))
    return presses

def solveWithSympy(machine: Machine):
    # promising but slow. Occcasionally can't find a valid solution
    # can reduce search space by finding the minimum joltage that each free button is connected to
    presses = sp.symbols(f"b_0:{len(machine.buttonwirings)}")
    equations = []
    pressMatrix = np.array(machine.buttonwirings).T
    for line, joltage in zip(pressMatrix, machine.joltages):
        text = " + ".join([f"b_{ind}" for ind, coef in enumerate(line) if coef > 0]) + f" - {joltage}"
        equation = sp.sympify(text)
        equations.append(equation)
    tqdm.write(str(equations))
    solutions = sp.linsolve(equations, presses) # TODO try evaluating by only increasing numbers?...
    solution = list(solutions)[0]
    tqdm.write(str(solution))
    answerExpression = sp.sympify(str(solution)[1:-1].replace(",", "+"))
    freevars = list(solutions.free_symbols)
    freevarscount = len(freevars)
    
    evalFn = sp.utilities.lambdify(freevars, solution)
    if freevarscount == 0:
        return solution
    maxJoltage = max(machine.joltages)
    tqdm.write(f"{freevarscount} {maxJoltage}")
    tqdm.write(str(answerExpression))
    
    return findCorrectAnswer(lambda x: evalFn(*x), np.arange(maxJoltage+1), freevarscount)

#TODO try solving with PULP
def solveWithPulp(machine: Machine):
    pressMatrix = np.array(machine.buttonwirings).T
    problem = pp.LpProblem("aoc10", pp.LpMinimize)
    maxJoltage = max(machine.joltages) #TODO can reduce this search space
    variables = [pp.LpVariable(f"b{ind}", 0, maxJoltage, cat="Integer") for ind in range(len(machine.buttonwirings))]
    problem += pp.lpSum(variables) #goal: minimize this
    for jnd, line in enumerate(pressMatrix):
        lineVars = [variables[ind] for ind, c in enumerate(line) if c > 0]
        problem += pp.LpConstraint(pp.lpSum(lineVars), sense=0, name=f"j{jnd}", rhs=machine.joltages[jnd])
    status = problem.solve()
    variableValues = tuple(pp.value(v) for v in variables)
    return variableValues
        
def findCorrectAnswer(evalFunction, valueRange, freevarscount):
    #TODO try plugging into a solver with constraints that minimizes the sum of button presses
    totry = np.array(np.meshgrid(*[valueRange for _ in range(freevarscount)])).T.reshape(-1, freevarscount)
    possibleAnswers = list(tqdm(map(evalFunction, totry), total=len(totry), desc="Calculating values"))
    answers = list(tqdm(map(lambda a: sum(a) if isAnswerValid(a) else np.inf, possibleAnswers), total=len(possibleAnswers), desc="Checking values"))
    argmin = np.argmin(answers)
    return possibleAnswers[argmin]

def isAnswerValid(answer):
    return all(v >= 0 and abs(v - int(v)) < 1e-6 for v in answer)

def getMachine(line):
    buttonWirings = []
    for segment in line.split():
        if segment[0] == "[":
            lightStates = tuple([1 if c == "#" else 0 for c in segment[1:-1]])
            lightNumber = int(''.join(map(str, lightStates)), 2)
        elif segment[0] == "{":
            joltages = tuple(map(int, segment[1:-1].split(",")))
        else:
            buttonWiring = set(map(int, segment[1:-1].split(",")))
            wiring = [1 if i in buttonWiring else 0 for i in range(len(lightStates))]
            buttonWirings.append(wiring)
            
    machine = Machine(lightNumber=lightNumber, buttonwirings=buttonWirings, joltages=joltages)
    return machine

def getJoltages(buttonWirings, buttonPresses):
    joltages = [0]*(max(max(b) for b in buttonWirings)+1)
    for ind, buttonPresses in enumerate(buttonPresses):
        for j in buttonWirings[ind]:
            joltages[j] += buttonPresses
    return tuple(joltages)

def getJoltagesFromPressMatrix(pressMatrix, buttonPresses):
    return np.matmul(pressMatrix, buttonPresses)

def getLines(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return [line.replace("\n", "") for line in f.readlines()]

def toArray(lines):
    return np.array([list(line) for line in lines])

if __name__ == "__main__":
    main()
    
# 21389 is too low
# 20638 is the value if invalid answers are skipped
# 21410 is also too low
# 21469