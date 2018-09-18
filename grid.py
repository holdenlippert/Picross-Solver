#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import intersection, validoptions, update, log

class Grid:
    symbols = {
        None: ' ',
        True: '▀',
        False: '·'
    }
    
    def __init__(self, size):
        self.size = size
        self.grid = [[None for i in range(size)] for j in range(size)]
        self.failedmoves = 0

    def __str__(self):
        return '\n'.join([' '.join([self.symbols[elem] for elem in line]) for line in self.grid])
    
    def setcolumn(self, vals, id):
        if len(vals) != self.size:
            print "Vals is wrong length.\nVals:%s\nSize:%d" % (vals, self.size)
            assert False
        for i, elem in enumerate(vals):
            self.grid[i][id] = elem

    def setrow(self, vals, id):
        if len(vals) != self.size:
            print "Vals is wrong length.\nVals:%s\nSize:%d" % (vals, self.size)
            assert False
        self.grid[id] = vals
        
    def getcolumn(self, id):
        column = []
        for line in self.grid:
            column.append(line[id])
        return column
    
    def getrow(self, id):
        return self.grid[id]
    
    def updatecolumn(self, specs, id):
        self.setcolumn(update(self.getcolumn(id), specs), id)
        return

    def oldupdatecolumn(self, specs, id):
        options = validoptions(self.getcolumn(id), specs)
        newrow = intersection(options)
        self.setcolumn(newrow, id)

    def updaterow(self, specs, id):
        self.setrow(update(self.getrow(id), specs), id)

    def oldupdaterow(self, specs, id):
        options = validoptions(self.getrow(id), specs)
        newrow = intersection(options)
        self.setrow(newrow, id)
    
    def isSolved(self):
        for line in self.grid:
            if None in line:
                return False
        return True

    def isUnsolved(self):
        return not self.isSolved()

def main():
    pass

if __name__ == "__main__":
    main()
