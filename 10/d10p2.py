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

verbose = False

Machine = namedtuple("Machine", ["lightNumber", "buttonwirings", "joltages"])

filenames = ["sample.txt", "input.txt"]

def main():
    for filename in filenames:
        print(filename)
        lines = getLines(filename)
        mainFunction(lines)

def mainFunction(lines):
    machines = list(map(getMachine, lines))
    buttonPressCounts = []
    for ind, m in enumerate(tqdm(machines, position=tqdm._get_free_pos(), desc="Calculation Progress")):
        if verbose:
            tqdm.write(f"{ind}: {m}")
        # presses = solveWithPulp(m)
        presses = solveWithSympy(m)
        pressSum = sum(presses)
        if verbose:
            tqdm.write(str(presses))
            tqdm.write(str(pressSum))
        if isAnswerValid(presses):
            buttonPressCounts.append(pressSum)
        else:
            tqdm.write(f"MACHINE {ind} HAS NO VALID SOLUTION!!!")
    print(round(int(sum(buttonPressCounts))))

def solveWithMatrices(machine: Machine):
    #gives floats and wrong answer
    pressMatrix = np.array(machine.buttonwirings).T
    leftInverse = np.linalg.pinv(pressMatrix)
    if verbose:
        tqdm.write(str(leftInverse))
    presses = np.matmul(leftInverse, np.array(machine.joltages))
    if verbose:
        tqdm.write(str(presses))
        tqdm.write(str(getJoltagesFromPressMatrix(pressMatrix, presses)))
    return presses

def solveWithSympy(machine: Machine):
    # can reduce search space by finding the minimum joltage that each free button is connected to
    presses = sp.symbols(f"b_0:{len(machine.buttonwirings)}")
    equations = []
    pressMatrix = np.array(machine.buttonwirings).T
    for line, joltage in zip(pressMatrix, machine.joltages):
        text = " + ".join([f"b_{ind}" for ind, coef in enumerate(line) if coef > 0]) + f" - {joltage}"
        equation = sp.sympify(text)
        equations.append(equation)
    if verbose:
        tqdm.write(str(equations))
    solutions = sp.linsolve(equations, presses)
    solution = list(solutions)[0]
    if verbose:
        tqdm.write(str(solution))
    answerExpression = sp.sympify(str(solution)[1:-1].replace(",", "+"))
    freevars = list(solutions.free_symbols)
    freevarscount = len(freevars)
    
    evalFn = sp.utilities.lambdify(freevars, solution)
    if freevarscount == 0:
        return solution
    maxJoltage = max(machine.joltages)
    if verbose:
        tqdm.write(f"{freevarscount} {maxJoltage}")
        tqdm.write(str(answerExpression))
    
    return findCorrectAnswer(lambda x: evalFn(*x), np.arange(maxJoltage+1), freevarscount)

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
    possibleAnswers = list(tqdm(map(evalFunction, totry), total=len(totry), desc="Calculating values", position=tqdm._get_free_pos()))
    answers = list(tqdm(map(lambda a: sum(a) if isAnswerValid(a) else np.inf, possibleAnswers), total=len(possibleAnswers), desc="Checking values", position=tqdm._get_free_pos()))
    argmin = np.argmin(answers)
    return possibleAnswers[argmin]

def isAnswerValid(answer):
    roundedAnswer = [round(n) for n in answer]
    return all(vr >= 0 and abs(v - vr) < 1e-6 for v, vr in zip(answer, roundedAnswer))

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