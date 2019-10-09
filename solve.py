#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os.path
from grid import Grid
from utils import solve
from reader import read_specs


def main(args):
    if len(args) != 2:
        print("Usage: %s [filename]" % args[0])
        return 1
    if not os.path.isfile(args[1]):
        print("Could not find file '%s'." % args[1])
        return 1

    colspecs, rowspecs, size = read_specs(args[1])
    G = Grid(size)
    solve(G, colspecs, rowspecs, watch=False)
    print(G)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
