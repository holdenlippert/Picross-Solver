#!/usr/bin/env python
import sys
from itertools import cycle
import time
LOG = True


def debugrecursion(f):
    """
    Decorator function; prints out inputs and outputs for
    a recursive function with padding so you can see the
    call tree's structure.
    """
    f.depth = 0 # tracks recursion depth
    def wrapped(*args, **kwargs):
        # print out arguments, padded by 'depth' many tabs
        pad = "|\t" * f.depth
        argstring = (str(args) if args else "")
        argstring += (str(kwargs) if kwargs else "")
        log(pad + "Arguments: " + argstring)
     
        # increase the depth while recursing; decrease it when finished
        f.depth += 1
        try:
            answer = f(*args, **kwargs)
        except Exception as e:
            f.depth -= 1
            log(pad + "Raising: " + e.message)
            raise e

        f.depth -= 1
         
        # print out the results, again padded by 'depth' many tabs
        log(pad + "Returning: " + str(answer))

        return answer
    return wrapped

class UnsolvableException(Exception):
    pass


def log(*messages):
    if LOG:
        print "Log:\t", ' '.join(map(str, messages))
    
def fits(row, specs):
    """
    Example inputs:
    row: [True, True, False, False, True]
    specs: [2, 1]
    """
    if len(specs) == 0:
        return True not in row
    blocksize, block = 0, 0
    for elem in row:
        blocksize += 1 if elem else 0
        if (not elem) and blocksize > 0:
            if block >= len(specs) or specs[block] != blocksize:
                return False
            blocksize, block = 0, block + 1
    if blocksize > 0:
        return specs[-1] == blocksize and block == len(specs) - 1
    return block == len(specs)

def intersection(options):
    if len(options) == 0:
        raise UnsolvableException
    intersect = []
    for i in range(len(options[0])):
        if len(set([option[i] for option in options])) != 1:
            intersect.append(None)
        else:
            intersect.append(options[0][i])
    return intersect

def alloptions(currentvals, i=0):
    celloptions = [True, False] if currentvals[i] is None else [currentvals[i]]
    if i == len(currentvals) - 1:
        return [[option] for option in celloptions]
    rowoptions = []
    for option in alloptions(currentvals, i+1):
        for celloption in celloptions:
            rowoptions.append([celloption] + option)
    return rowoptions

def validoptions(currentvals, spec):
    if spec == []:
        return [[False] * len(currentvals)]
    options = alloptions(currentvals)
    return [option for option in options if fits(option, spec)]

#@debugrecursion
def leftmost(currentvals, spec):
    if spec == []:
        if True in currentvals:
            raise UnsolvableException, "True in currentvals"
        return [False] * len(currentvals)

    if currentvals == [] or spec[0] > len(currentvals):
        raise UnsolvableException, "Ran out of currentvals: " + str((currentvals, spec))

    if spec[0] == len(currentvals):
        if False in currentvals:
            raise UnsolvableException, "False blocking trues: " + str((currentvals, spec))
        return [True] * spec[0]

    if False in currentvals[:spec[0]]:
        if True in currentvals[:currentvals.index(False)]:
            raise UnsolvableException, "False blocking trues: " + str((currentvals, spec))
        rest = leftmost(currentvals[currentvals.index(False) + 1:], spec)
        return [False] * (currentvals.index(False) + 1) + rest

    if currentvals[0] == True:
        rest = leftmost(currentvals[spec[0] + 1:], spec[1:])
        return [True] * spec[0] + [False] + rest

    if currentvals[spec[0]] == True:
        rest = leftmost(currentvals[1:], spec)
        return [False] + rest

    try:
        rest = leftmost(currentvals[spec[0] + 1:], spec[1:])
    except UnsolvableException:
        rest = leftmost(currentvals[1:], spec)
        return [False] + rest
    return [True] * spec[0] + [False] + rest

def rightmost(currentvals, spec):
    rcurrentvals = list(reversed(currentvals))
    rspec = list(reversed(spec))
    return list(reversed(leftmost(rcurrentvals, rspec)))

def update(currentvals, spec):
    lvals = leftmost(currentvals, spec)
    rvals = rightmost(currentvals, spec)
    vals = []

    lblock, rblock = 0, 0
    for i in range(1, len(currentvals)):
        if lvals[i - 1:i + 1] == [True, False]:
            lblock += 1
        if rvals[i - 1:i + 1] == [True, False]:
            rblock += 1
        if lblock == rblock and lvals[i] == rvals[i]:
            vals.append(lvals[i])
        else:
            vals.append(None)
    
    if lvals[0] == rvals[0]:
        vals.insert(0, lvals[0])
    else:
        vals.insert(0, None)

    for i, elem in enumerate(currentvals):
        if elem is not None:
            vals[i] = elem
    return vals

def solve(grid, colspecs, rowspecs, watch=False):
    for i in cycle(range(2 * grid.size)):
        if grid.isSolved():
            if watch:
                print "Solved it!\n"
            break
        if i % 2 == 0:
            grid.updatecolumn(colspecs[i/2], i/2)
        else:
            grid.updaterow(rowspecs[i/2], i/2)
        time.sleep(.01 if watch else 0)
        if watch:
            print "\n" * 100, grid



