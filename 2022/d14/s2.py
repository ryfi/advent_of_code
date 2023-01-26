"""
--- Part Two ---
You realize you misread the scan. There isn't an endless void at the bottom of the scan - there's floor, and you're standing on it!

You don't have time to scan the floor, so assume the floor is an infinite horizontal line with a y coordinate equal to two plus the highest y coordinate of any point in your scan.

In the example above, the highest y coordinate of any point is 9, and so the floor is at y=11. (This is as if your scan contained one extra rock path like -infinity,11 -> infinity,11.) With the added floor, the example above now looks like this:

        ...........+........
        ....................
        ....................
        ....................
        .........#...##.....
        .........#...#......
        .......###...#......
        .............#......
        .............#......
        .....#########......
        ....................
<-- etc #################### etc -->
To find somewhere safe to stand, you'll need to simulate falling sand until a unit of sand comes to rest at 500,0, blocking the source entirely and stopping the flow of sand into the cave. In the example above, the situation finally looks like this after 93 units of sand come to rest:

............o............
...........ooo...........
..........ooooo..........
.........ooooooo.........
........oo#ooo##o........
.......ooo#ooo#ooo.......
......oo###ooo#oooo......
.....oooo.oooo#ooooo.....
....oooooooooo#oooooo....
...ooo#########ooooooo...
..ooooo.......ooooooooo..
#########################
Using your scan, simulate the falling sand until the source of the sand becomes blocked. How many units of sand come to rest?
"""
import numpy as np
from s1 import plot_rocks


def move_sand(cave_grid, starting_position):
    if starting_position == (500, -1):
        return False
    below = cave_grid[starting_position[1] + 1, starting_position[0]]
    left = cave_grid[starting_position[1] + 1, starting_position[0] - 1]
    right = cave_grid[starting_position[1] + 1, starting_position[0] + 1]
    if not below:
        return move_sand(cave_grid, starting_position=(starting_position[0], starting_position[1] + 1))
    elif not left:
        return move_sand(cave_grid, starting_position=(starting_position[0] - 1, starting_position[1] + 1))
    elif not right:
        return move_sand(cave_grid, starting_position=(starting_position[0] + 1, starting_position[1] + 1))
    else:
        cave_grid[starting_position[1], starting_position[0]] = 2
        return True


if __name__ == '__main__':
    rock_scan = []
    max_x = 0
    max_y = 0
    with open('input.txt') as f:
        for line in f:
            # split, convert to ints, then to numpy arrays for easy subtraction
            rock_scan.append([list(map(int, x.split(','))) for x in line.strip().split(' -> ')])
            running_max_x = max([x[0] for x in rock_scan[-1]])
            running_max_y = max([x[1] for x in rock_scan[-1]])
            if max_x < running_max_x:
                max_x = running_max_x
            if max_y < running_max_y:
                max_y = running_max_y
    cave_grid = np.zeros(shape=(max_y + 3, max_x * 2), dtype=np.int8)
    plot_rocks(rock_scan=rock_scan, cave_grid=cave_grid)
    cave_grid[-1, :] = 1
    sand_start = (500, np.argmax(cave_grid[:, 500] > 0) - 1)
    sand_count = 0
    sand_moving = True
    while sand_moving:
        sand_moving = move_sand(cave_grid, sand_start)
        if sand_moving:
            sand_count += 1
            sand_start = (500, np.argmax(cave_grid[:, 500] > 0) - 1)
    print(sand_count)
