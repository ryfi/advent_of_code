"""
--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a. The goal is still the square marked E. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a, plus the square marked S that counts as being at elevation a). If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?
"""

import numpy as np
from s1 import bfs

if __name__ == '__main__':
    input_data = []
    heightmap = []
    with open('input.txt') as f:
        for line in f:
            input_data.append([x for x in line.strip()])
            heightmap.append([ord(x) for x in line.strip()])

    heightmap = np.array(heightmap)
    start = np.where(heightmap == 83)
    start_coord = (start[0][0], start[1][0])
    end = np.where(heightmap == 69)
    end_coord = (end[0][0], end[1][0])
    heightmap[start_coord] = 97
    heightmap[end_coord] = 123

    a_position = np.where(heightmap == 97)
    a_position_coords = list(zip(a_position[0], a_position[1]))

    possible_start_distances = []
    for possible_start in a_position_coords:
        possible_start_distances.append(bfs(root=possible_start,
                                            searched=end_coord,
                                            input_data=heightmap))
    print(min(x for x in possible_start_distances if x is not None))
