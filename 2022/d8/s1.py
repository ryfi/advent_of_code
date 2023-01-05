"""
--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30373
25512
65332
33549
35390
Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?
"""

import numpy as np

if __name__ == '__main__':
    grid = []
    with open('input.txt') as f:
        for line in f:
            grid.append(np.array([*line.strip()]).astype(np.int8))
    grid = np.asarray(grid)

    hidden_count = 0
    colored_representation = ''

    for row_num in range(0, 99):
        for col_num in range(0, 99):

            left = grid[row_num, :col_num]
            right = grid[row_num, col_num + 1:]
            above = grid[:row_num, col_num]
            below = grid[row_num + 1:, col_num]
            current = grid[row_num, col_num]

            taller_left = False
            if len(left) > 0 and np.amax(left) >= current:
                taller_left = True

            taller_right = False
            if len(right) > 0 and np.amax(right) >= current:
                taller_right = True

            taller_above = False
            if len(above) > 0 and np.amax(above) >= current:
                taller_above = True

            taller_below = False
            if len(below) > 0 and np.amax(below) >= current:
                taller_below = True

            if taller_right and taller_left and taller_above and taller_below:
                hidden_count += 1
                colored_representation += f'\x1b[0;30;41m{str(grid[row_num, col_num])}\x1b[0m'
            else:
                colored_representation += f'{str(grid[row_num, col_num])}'
        colored_representation += '\n'
    print(colored_representation)
    print(f'{hidden_count=}')
