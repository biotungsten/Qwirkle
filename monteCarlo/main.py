import itertools as iter
import logging
import numpy as np
import random
from scipy import special
from functools import lru_cache
import warnings
import time
import matplotlib.pyplot as plt

logging.info("Started program.")
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', filename='log{}.log'.format(int(time.time())), level=logging.INFO)


@lru_cache(maxsize=10000)
def binc(n, k):
    return special.binom(n,k)
    
def randomIntGaussian(lb, ub):
    g = random.gauss((lb+ub)/2, (lb-(lb+ub)/2)/4)
    i = int(g)
    return min(max(lb,i),ub)

def generateSplitSet(conditionals, totalSize, condDuplets, condTriplets):
    logging.debug("Called generateSplitSet.")
    remainingSize = totalSize - conditionals
    if 2 * condDuplets + 3 * condTriplets > conditionals:
        logging.error(f"Stone set of size {totalSize} with {conditionals} conditionals is too small for {condDuplets} duplets and {condTriplets} triplets.")
    else:
        set = []
        condChars = []
        numberOfSingleStones = conditionals - (2 * condDuplets + 3 * condTriplets)
        n = 0
        for m in range(condDuplets):
            condChars.append(chr(n+65))
            set.append(chr(n+65)+"1")
            set.append(chr(n+65)+"2")
            n +=1
        for m in range(condTriplets):
            condChars.append(chr(n+65))
            set.append(chr(n+65)+"1")
            set.append(chr(n+65)+"2")
            set.append(chr(n+65)+"3")
            n +=1
        for m in range(numberOfSingleStones):
            condChars.append(chr(n+65))
            set.append(chr(n+65)+"1")
            n += 1
        for m in range(remainingSize):
            set.append(chr(n+65)+"1")
            n += 1
        logging.debug(f"Generated stone set. (set:{set}, condChars:{condChars})")
        return (set, condChars)

def countUniqueStonesInList(list):
    length = len(set([n[0] for n in list]))
    return length

def listContainsNUniqueConditionals(list, condChars):
    tempList = [n for n in list if n[0] in condChars]
    return countUniqueStonesInList(tempList)

def checkListsForContainingNUnique(size, sizeOfConditionals, sizeOfDraw, duplets, triplets):
    logging.debug("Called checkListsForContainingNUnique.")
    sourceSet, condChars= generateSplitSet(sizeOfConditionals, size, duplets, triplets)
    possibleHands = iter.combinations(sourceSet, sizeOfDraw)
    matching = [0,0,0,0,0,0,0]
    logging.debug(f"Check {binc(len(sourceSet), sizeOfDraw)} hand.")
    for hand in possibleHands:
        uniq = listContainsNUniqueConditionals(hand, condChars)
        if uniq < 0 or uniq > 6: logging.error(f"False uniq in hand {hand}")
        matching[uniq] += 1
    return matching

def M(k2, b, i, j, e, f, g):
    logging.debug("Called M.")
    logging.debug(f"Parameters - k: {k2}, b: {b}, i: {i}, j: {j}, e(T3): {e}, f(T2): {f}, g(D2): {g}.")
    if (k2 < 0) or (b < 0) or (i < 0) or (j < 0):
        logging.warning(f"Function called with negative arguments. Returning 0.")
        return 0
    if (e + f > j) or (g > i):
        logging.warn(f"(e, f, g) - ({e}, {f}, {g}) not compatible with (i, j) - ({i}, {j}). Returning 0.")
        return 0
    if (b-(2*g+3*f+3*e)-(i-g)-(j-(e+f))*2<k2-(2*g+2*f+3*e)):
        logging.debug("Impossible combination of e,f,g and i,j. Returning 0.")
        return 0

    b_c = b  - (2*g+3*f+3*e)
    k_c = k2 - (2*g+2*f+3*e)
    i_c = i  - g
    j_c = j  - (e+f)

    mz = sum([binc(i_c,l)*binc(j_c,h)*binc(b_c-2*i_c-3*j_c, k_c-l-h)*2**l*3**h for l in range(0,i_c+1) for h in range(0,j_c+1)])
    
    d2 = binc(i,g)
    t3 = binc(j,e)
    t2 = binc(j-e, f)*3**f
    logging.debug(f"Calculated following components - d2: {d2}, t2: {t2}, t3: {t3}, mz: {mz}")
    
    number = d2*t3*t2*mz
    return number

def generateEFG(noOfDraw, noOfUniques, noOfDuplets, noOfTriplets):
    logging.debug("Called generateEFG.")
    logging.debug(f"Parameters - noOfDraw: {noOfDraw}, noOfUniques: {noOfUniques}, i: {noOfDuplets}, j: {noOfTriplets}.")
    sets = [(e,f,g) for e in range(0,noOfTriplets+1) for f in range(0,noOfTriplets+1) for g in range(0, noOfDuplets+1)]
    valid = []
    for s in sets:
        e,f,g = s[0], s[1], s[2]
        if (noOfDraw-(2*e+f+g)==noOfUniques) and (e+f <= noOfTriplets) and (g <= noOfDuplets):
            valid.append(s)
    logging.debug(f"Generated following sets {sets}.")
    return valid

def NUnique(noOfDraw, noOfStones, noOfDuplets, noOfTriplets, noOfUniques):
    logging.debug("Called NUnique.")
    logging.debug(f"Parameters - noOfDraw: {noOfDraw}, noOfStones: {noOfStones}, noOfUniques: {noOfUniques}, i: {noOfDuplets}, j: {noOfTriplets}.")
    efgs = generateEFG(noOfDraw, noOfUniques, noOfDuplets, noOfTriplets)
    no = 0
    for s in efgs:
        e,f,g = s[0], s[1], s[2]
        local = M(noOfDraw, noOfStones, noOfDuplets, noOfTriplets, e, f, g)
        no += local
    return no

def N(sizeOfDraw, availableStones, conditionalsAmongStones, numberOfDuplets, numberOfTriplets, wishedNumber):
    logging.debug("Called N.")
    logging.debug(f"Parameters - conds: {conditionalsAmongStones}, k: {sizeOfDraw}, noOfStones: {availableStones}, noOfUniques: {wishedNumber}, i: {numberOfDuplets}, j: {numberOfTriplets}.")
    n = 0
    for firstHalfSize in range(wishedNumber, min(sizeOfDraw+1, conditionalsAmongStones+1)):
        firstHalfN = NUnique(firstHalfSize, conditionalsAmongStones, numberOfDuplets, numberOfTriplets, wishedNumber)
        local = firstHalfN*binc(availableStones-conditionalsAmongStones, sizeOfDraw-firstHalfSize)
        n += local
    logging.debug(f"Calculated {n} as result.")
    return n

@lru_cache(maxsize=20)
def generateTripDup(conds):
    return [(n,m,k) for n in range(0,7) for m in range(0,7-n) for k in range(0,7-n-m) if n+2*m+3*k == conds]

def main():
    n = 0
    no = 5000
    while n<no:
        logging.info(f"Iteration {n} started.")
        availableStones = random.randint(10,25)
        conditionalsAmongStones = randomIntGaussian(0,min(availableStones,19))
        sizeOfDraw = randomIntGaussian(0,availableStones)
        opts = generateTripDup(conditionalsAmongStones)
        parms = random.choice(opts)
        numberOfDuplets, numberOfTriplets = parms[1], parms[2]
        logging.info(f"Generated following random parameters - available: {availableStones}, conditionals: {conditionalsAmongStones}, draw: {sizeOfDraw}, i: {numberOfDuplets}, j: {numberOfTriplets}")

        sums = [0,0]
        exacts = checkListsForContainingNUnique(availableStones, conditionalsAmongStones, sizeOfDraw, numberOfDuplets, numberOfTriplets)
        for wishedNumber in range(0,7):
            logging.debug(f"Calculation for wished {wishedNumber} started.")
            exact = exacts[wishedNumber]
            predicted = N(sizeOfDraw, availableStones, conditionalsAmongStones, numberOfDuplets, numberOfTriplets, wishedNumber)
            sums[0] += exact
            sums[1] += predicted
            logging.debug(f"exact vs. predicted :{int(exact)}|{int(predicted)}") 
        logging.info(f"Sum of exact is {sums[0]}, of predicted is {sums[1]} - required is {binc(availableStones, sizeOfDraw)}")
        if [n/binc(availableStones, sizeOfDraw) for n in sums] != [1.0, 1.0]:
            logging.error("N not sum 1.")
        if int(exact) != int(predicted):
            logging.error(f"N not correct.")
        n += 1
        print(round(n/no,5))
    return 0
    
if __name__ == "__main__":
    main()