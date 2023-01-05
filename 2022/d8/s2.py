"""
--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390
Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390
Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?
"""

import numpy as np


def viewing_dist(arr: np.ndarray, tree_height: np.int8):
    distance = np.argmax(arr >= tree_height)
    if distance == 0:
        if arr[0] >= tree_height:
            return 1
        else:
            return len(arr)
    else:
        return distance + 1


if __name__ == '__main__':
    grid = []
    with open('input.txt') as f:
        for line in f:
            grid.append(np.array([*line.strip()]).astype(np.int8))
    grid = np.asarray(grid)

    most_scenic = 0
    scenic_position = (0, 0)

    for row_num in range(1, 98):
        for col_num in range(1, 98):

            current = grid[row_num, col_num]

            left = viewing_dist(grid[row_num, :col_num][::-1], current)
            right = viewing_dist(grid[row_num, col_num + 1:], current)
            above = viewing_dist(grid[:row_num, col_num][::-1], current)
            below = viewing_dist(grid[row_num + 1:, col_num], current)

            scenic_score = left * right * above * below
            if scenic_score > most_scenic:
                most_scenic = scenic_score
                scenic_position = (row_num, col_num)
    print(f'{most_scenic=}')
    print(f'{scenic_position=}')
