#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest, sys
from grid import Grid
import utils
import reader
from utils import leftmost, rightmost, update
from itertools import cycle


focus_on_left = False

class TestGrid(unittest.TestCase):
    def setUp(self):
        self.size = 10
        self.testrow = [None, True, None, False, True, None, False, None, None, True]
        self.grid = Grid(self.size)


    def test_is_solved(self):
        self.assertFalse(self.grid.isSolved())
        for i in range(self.size):
            self.grid.setcolumn([True] * self.size, i)
        self.assertTrue(self.grid.isSolved())


    def test_get_and_set_row_and_column(self):
        self.grid.setcolumn(self.testrow, 3)
        self.assertEqual(self.grid.getcolumn(3), self.testrow)
        self.assertEqual(self.grid.getrow(3), [None] * 3 + [False] + [None] * 6)
        self.assertEqual(self.grid.getrow(1), [None] * 3 + [True] + [None] * 6)
        self.assertEqual(self.grid.getrow(2), [None] * 10)


    def test_update_column(self):
        self.grid.updatecolumn([1], 0)
        self.assertEqual(self.grid.getcolumn(0), [None] * 10)
        self.grid.updatecolumn([10], 1)
        self.assertEqual(self.grid.getcolumn(1), [True] * 10)
        self.grid.updatecolumn([], 2)
        self.assertEqual(self.grid.getcolumn(2), [False] * 10)
        self.grid.updatecolumn([4, 4], 3)
        self.assertEqual(self.grid.getcolumn(3), [None, True, True, True, None, None, True, True, True, None])
        self.grid.updatecolumn([2, 1, 2, 2], 4)
        self.assertEqual(self.grid.getcolumn(4), [True, True, False, True, False, True, True, False, True, True])
        

    def test_update_row(self):
        self.grid.updaterow([1], 0)
        self.assertEqual(self.grid.getrow(0), [None] * 10)
        self.grid.updaterow([10], 1)
        self.assertEqual(self.grid.getrow(1), [True] * 10)
        self.grid.updaterow([], 2)
        self.assertEqual(self.grid.getrow(2), [False] * 10)
        self.grid.updaterow([4, 4], 3)
        self.assertEqual(self.grid.getrow(3), [None, True, True, True, None, None, True, True, True, None])
        self.grid.updaterow([2, 1, 2, 2], 4)
        self.assertEqual(self.grid.getrow(4), [True, True, False, True, False, True, True, False, True, True])


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.rows = [
            [True, True, False, False, True, False], # 0
            [False, False, True, True, False, True],
            [False, False, True, True, False, True],
            [False, True, True, False, False, False],
            [False, True, False, True, False, False],
            [None] * 7, # 5
            [None, True, False, True, True, None],
            [None, True, None, False, None, True],
            [False, True, True, False, True, False, False, True, False, True],
            [True, True, True, False, True, False, False, True, False, True],
            [False, True, True, True, False, True, False, True, False, True], # 10
            [False] + [True] * 9,
            [True, True, False, False, True, False, False, False, False, True],
            [True, True, False, False, True, False, False, True, False, True],
            [False, True, True, False, True, True, False, False, True, True],
            [False] * 10, # 15
            [True] * 10,
        ]


    def test_intersection(self):
        inputoutput = [
            ([0, 1], [None] * 6),
            ([1, 2], [False, False, True, True, False, True]),
            ([2, 3], [False, None, True, None, False, None]),
            ([2, 3, 4], [False, None, None, None, False, None]),
        ]
        for inp, out in inputoutput:
            args = [self.rows[j] for j in inp]
            self.assertEqual(utils.intersection(args), out)


    def test_all_options(self):
        inputoutput = [
            (0, 1),
            (5, 128),
            (6, 4),
            (7, 8),
        ]
        for inp, out in inputoutput:
            self.assertEqual(len(utils.alloptions(self.rows[inp])), out)


    def test_good_fits(self):
        inputs = [
            (8, [2, 1, 1, 1]),
            (15, [])
        ]
        for row, spec in inputs:
            self.assertTrue(utils.fits(self.rows[row], spec))


    def test_bad_fits(self):
        inputs = [
            (9, [2, 1, 1, ]),
            (10, [2, 1, 1, 1]),
            (11, [6, 3]),
            (12, [2, 1, 1, 1]),
            (16, [])
        ]
        for row, spec in inputs:
            self.assertFalse(utils.fits(self.rows[row], spec))


    def test_valid_options(self):
        row = [None, True, None, False, True, None, False, None, None, True]
        inputoutput = [
            ([2, 1, 1], 2),
            ([2, 1, 2], 2),
            ([3, 1, 2], 1),
        ]
        for inp, out in inputoutput:
            self.assertEqual(len(utils.validoptions(row, inp)), out)
        row = [None, None, True, None, None, None]
        inputoutput = [
            ([3], 3),
            ([1, 1, 1], 2),
            ([2, 1], 3),
        ]
        for inp, out in inputoutput:
            self.assertEqual(len(utils.validoptions(row, inp)), out)
        row = [None] * 10
        inputoutput = [
            ([3, 6], 1),
        ]
        for inp, out in inputoutput:
            self.assertEqual(len(utils.validoptions(row, inp)), out)


    def test_read_specs(self):
        colspecs, rowspecs, size = reader.read_specs("testspecs.txt")
        self.assertEqual(colspecs, [[3, 5], [4, 3], [4, 1], [4, 3, 2], [4, 3, 1], [3, 3, 2], [3, 5, 3, 1], [1, 4, 2, 3], [2, 2, 2, 2, 1], [2, 1, 1], [1, 1, 2], [1, 1, 1, 1], [2, 1, 2, 1], [4, 8], [4, 1, 1]])
        self.assertEqual(rowspecs, [[5, 4], [9, 1], [6, 4], [5, 1, 3], [2, 3, 2], [1, 2, 2, 2], [7], [6, 2], [2, 2], [7], [1, 3, 2], [2, 1, 1], [2, 3, 1], [2, 3, 4, 1], [1, 1, 2, 4]])
        self.assertEqual(size, 15)


    def test_leftmost(self):
        row = [None] * 2
        self.assertEqual(leftmost(row, [1]), [True, False])

        row = [None, True]
        self.assertEqual(leftmost(row, [1]), [False, True])

        row = [True, None]
        self.assertEqual(leftmost(row, [1]), [True, False])

        row = [None] * 4
        self.assertEqual(leftmost(row, [1, 1]), [True, False, True, False])
        self.assertEqual(leftmost(row, [2]), [True, True, False, False])

        row = [None, True, None, False, True, None, False, None, None, True]
        self.assertEqual(leftmost(row, [2, 1, 1]),
            [True, True, False, False, True, False, False, False, False, True])
        self.assertEqual(leftmost(row, [2, 1, 2]),
            [True, True, False, False, True, False, False, False, True, True])
        self.assertEqual(leftmost(row, [3, 1, 2]),
            [True, True, True, False, True, False, False, False, True, True])

        row = [True, False, None, True, None]
        with self.assertRaises(utils.UnsolvableException):
            leftmost(row, [2])

        row = [True, None, None, False, None, True, False, None, True, None]
        self.assertEqual(leftmost(row, [1, 1, 2]),
            [True, False, False, False, False, True, False, True, True, False])

        row = [None, True, None, None]
        self.assertEqual(leftmost(row, [1]), [False, True, False, False])

        row = [None, None, True, None, None]
        self.assertEqual(leftmost(row, [2]), [False, True, True, False, False])

        row = [None, False, None, True, None, None, None]
        self.assertEqual(leftmost(row, [4]), [False, False, True, True, True, True, False])

        row = [None, None, None, True, None, False, None, None, None, False,
               None, True, None, None, None]
        self.assertEqual(leftmost(row, [3, 1, 4]),
            [False, True, True, True, False, False, True, False, False, False,
             True, True, True, True, False])

        row = [True, None, None, False, None, True, False, None, True, None]
        self.assertEqual(leftmost(row, [1, 1, 2]),
            [True, False, False, False, False, True, False, True, True, False])

        row = [False, None, None, True, None, False, None, None, None, False,
               None, True, False, False, None]
        self.assertEqual(leftmost(row, [3, 1, 1]),
            [False, True, True, True, False, False, True, False, False, False,
             False, True, False, False, False])

        row = [False, None, None, True, True, None, None, False, True, None,
               False, None, True, True, True]
        self.assertEqual(leftmost(row, [1, 2, 2, 3]), 
            [False, True, False, True, True, False, False, False, True, True,
             False, False, True, True, True])

        row = [True, True, None, None, False]
        self.assertEqual(leftmost(row, [2, 1]), [True, True, False, True, False])

        row = [True, True, True, None, False, None, True, False, None, None,
               True, True, None, None, False]
        self.assertEqual(leftmost(row, [3, 2, 2, 1]), 
            [True, True, True, False, False, True, True, False, False, False,
             True, True, False, True, False])

        row = [None, None, False, None, None, None, None, False, False, True,
               None, None, None, True, None]
        self.assertEqual(leftmost(row, [2, 1, 1]),
            [True, True, False, False, False, False, False, False, False, True,
             False, False, False, True, False])

        row = [None, None, True, False, False, None, None, None, None, False,
               None, None]
        self.assertEqual(leftmost(row, [1, 2]),
            [False, False, True, False, False, True, True, False, False, False, False, False])

        row = [None, True, None, None, None, True, False, False, None, None, None, None, False, None, None] 
        self.assertEqual(leftmost(row, [1, 1, 2]),
            [False, True, False, False, False, True, False, False, True, True, False, False, False, False, False])

    @unittest.skipIf(focus_on_left, "")
    def test_rightmost(self):
        row = [None] * 2
        self.assertEqual(rightmost(row, [1]), [False, True])

        row = [None, True]
        self.assertEqual(rightmost(row, [1]), [False, True])

        row = [True, None]
        self.assertEqual(rightmost(row, [1]), [True, False])

        row = [None] * 4
        self.assertEqual(rightmost(row, [1, 1]), [False, True, False, True])
        self.assertEqual(rightmost(row, [2]), [False, False, True, True])

        row = [None, True, None, False, True, None, False, None, None, True]
        self.assertEqual(rightmost(row, [2, 1, 1]),
            [False, True, True, False, True, False, False, False, False, True])
        self.assertEqual(rightmost(row, [2, 1, 2]),
            [False, True, True, False, True, False, False, False, True, True])
        self.assertEqual(rightmost(row, [3, 1, 2]),
            [True, True, True, False, True, False, False, False, True, True])

        row = [None, None, None, True, None, False, None, None, None, False,
               None, True, None, None, None]
        self.assertEqual(rightmost(row, [3, 1, 4]),
            [False, False, True, True, True, False, False, False, True, False,
             False, True, True, True, True])

        row = [False, None, None, True, None, False, None, None, None, False,
               None, True, False, False, None]
        self.assertEqual(rightmost(row, [3, 1, 1]),
            [False, False, True, True, True, False, False, False, False, False,
             False, True, False, False, True])

        row = [False, None, None, True, True, None, None, False, True, None,
               False, None, True, True, True]
        self.assertEqual(rightmost(row, [1, 2, 2, 3]),
            [False, True, False, True, True, False, False, False, True, True,
             False, False, True, True, True])

        row = [None, None, False, None, None, None, None, False, False, True,
               None, None, None, True, None]
        self.assertEqual(rightmost(row, [2, 1, 1]),
            [False, False, False, False, False, True, True, False, False, True,
             False, False, False, True, False])

    @unittest.skipIf(focus_on_left, "")
    def test_update(self):
        row = [None, None, None]
        self.assertEqual(update(row, [2]), [None, True, None])

        row = [None, True, None, None]
        self.assertEqual(update(row, [2]), [None, True, None, False])

        row = [None] * 10
        self.assertEqual(update(row, [4, 5]), [True] * 4 + [False] + [True] * 5)

        row = [None, None, True, None, False]
        self.assertEqual(update(row, [3]), [None, True, True, None, False])

        row = [None, None, None, True, None, False, None, None, None, False, None, True, None, None, None]
        expected = [False, None, True, True, None, False, None, None, None, False, None, True, True, True, None]
        self.assertEqual(update(row, [3, 1, 4]), expected)

        row = [False, None, None, True, None, False, None, None, None, False, None, True, False, False, None]
        expected = [False, None, True, True, None, False, None, None, None, False, None, True, False, False, None]
        self.assertEqual(update(row, [3, 1, 1]), expected)

        
        row = [False, None, None, True, True, None, None, False, True, None, False, None, True, True, True]
        expected = [False, True, False, True, True, False, False, False, True, True, False, False, True, True, True]
        self.assertEqual(update(row, [1, 2, 2, 3]), expected)

        row = [None, None, False, None, None, None, None, False, False, True, None, None, None, True, None]
        expected = [None, None, False, None, None, None, None, False, False, True, False, False, False, True, False]
        self.assertEqual(update(row, [2, 1, 1]), expected)


@unittest.skipIf(focus_on_left, "")
class TestSolver(object):
    def agree(self, solvedrow, guessrow):
        for solution, guess in zip(solvedrow, guessrow):
            if guess == (not solution):
                return False
        return True

    def getSolution(self):
        self.colspecs, self.rowspecs, self.size = reader.read_specs(self.testfile)
        G = Grid(self.size)
        for i in cycle(list(range(2 * self.size))):
            if G.isSolved():
                break
            if i % 2 == 0:
                G.oldupdatecolumn(self.colspecs[i/2], i/2)
            else:
                G.oldupdaterow(self.rowspecs[i/2], i/2)
        print("\n", G)
        return G

    def test_solver(self):
        solution = self.getSolution()
        G = Grid(self.size)
        for i in cycle(list(range(2 * self.size))):
            if G.isSolved():
                break
            if i % 2 == 0:
                try:
                    newcol = update(G.getcolumn(i/2), self.colspecs[i/2])
                    msg = "Column %d:\n%s\nupdated to:\n%s\nwith:%s"
                    self.assertTrue(self.agree(solution.getcolumn(i/2), newcol),
                            msg=msg % (i/2, G.getcolumn(i/2), newcol, self.colspecs[i/2]))
                    G.setcolumn(newcol, i/2)
                except utils.UnsolvableException as e:
                    msg = "Caught exception trying to update %s with %s:\n"
                    self.fail(msg % (G.getcolumn(i/2), self.colspecs[i/2]) + e.message)
            else:
                try:
                    newrow = update(G.getrow(i/2), self.rowspecs[i/2])
                    msg = "Row %d:\n%s\nupdated to:\n%s\nwith:%s"
                    self.assertTrue(self.agree(solution.getcolumn(i/2), newcol),
                            msg=msg % (i/2, G.getrow(i/2), newrow, self.rowspecs[i/2]))
                    G.setrow(newrow, i/2)
                except utils.UnsolvableException as e:
                    msg = "Caught exception trying to update %s with %s:\n"
                    self.fail(msg % (G.getcolumn(i/2), self.colspecs[i/2]) + e.message)
        self.assertEqual(solution.grid, G.grid)


def parametrize(BaseTest, attributename, attributevals):
    for i, val in enumerate(attributevals):
        name = BaseTest.__name__ + str(i)
        globals()[name] = type(name, (BaseTest, unittest.TestCase), {attributename: val})


parametrize(TestSolver, "testfile", ["testspecs.txt", "specs.txt"])



if __name__ == "__main__":
    unittest.main(verbosity=4)
