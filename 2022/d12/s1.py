"""
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device, but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that should get the best signal (E). Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be at most one higher than the elevation of your current square; that is, if your current elevation is m, you could step to elevation n, but not to elevation o. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^
In the above diagram, the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>). The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?
"""

import numpy as np
from collections import deque


def connected_neighbors(node: tuple, grid: np.ndarray) -> tuple[int, tuple[int, int], int]:
    for direction in [
        (node[0] + 1, node[1]),  # down
        (node[0] - 1, node[1]),  # up
        (node[0], node[1] + 1),  # right
        (node[0], node[1] - 1)  # left
    ]:
        if direction[0] < 0 or direction[1] < 0:
            # print('skip')
            continue
        elif direction[0] > grid.shape[0] - 1 or direction[1] > grid.shape[1] - 1:
            continue
        delta = grid[direction] - grid[node]
        yield grid[direction], direction, delta


def plot_navigable_neighbors(grid: np.ndarray) -> dict[tuple[int, int], list[tuple[int, int]]]:
    navigable_neighbors = {}
    for a in range(grid.shape[0]):
        for b in range(grid.shape[1]):
            navigable_neighbors[(a, b)] = []
            for dir_val, direction, delta in connected_neighbors((a, b), grid):
                if delta <= 1:
                    navigable_neighbors[(a, b)].append(direction)
    return navigable_neighbors


def find_path(position: tuple, heightmap: np.ndarray, steps: int, previous_moves: set = None):
    print(f'{position=}, {steps=}')
    if heightmap[position] == 124:
        print('found')
        return steps
    else:
        # rec_steps = steps
        if previous_moves is None:
            previous_moves = set()
        for dir_val, direction, delta in connected_neighbors(node=position, grid=heightmap):
            if (position, direction) in previous_moves:
                print(f'dead end, {(position, direction)}, {delta}')
                continue
            if delta <= 1:
                print(dir_val, position, direction, delta)
                previous_moves.add((position, direction))
                step_count = find_path(position=direction,
                                       heightmap=heightmap,
                                       steps=steps + 1,
                                       previous_moves=previous_moves)
                return step_count, previous_moves
            else:
                continue


def dfs(visited: set,
        graph: dict[tuple[int, int], list[tuple[int, int]]],
        node: tuple[int, int],
        steps: int = 0):
    if node not in visited:
        print(node, steps)
        visited.add(node)
        if node == (20, 68):
            print('FOUND END', steps)
        if node == (20, 0):
            print('FOUND START', steps)
        for neighbor in graph[node]:
            dfs(visited=visited, graph=graph, node=neighbor, steps=steps + 1)


def dfs_limited(visited: set,
                graph: dict[tuple[int, int], list[tuple[int, int]]],
                node: tuple[int, int],
                steps: int,
                max_depth: int,
                cur_depth: int):
    # print(node)
    if node in visited:
        return None
    visited.add(node)
    if node == (20, 68):
        print('FOUND END', steps)
        return node
    if cur_depth >= max_depth:
        return None
    # print(node, visited, steps, max_depth, cur_depth)
    for neighbor in graph[node]:
        # print(neighbor)
        found = dfs_limited(visited=visited,
                            graph=graph,
                            node=neighbor,
                            steps=steps + 1,
                            max_depth=max_depth,
                            cur_depth=cur_depth + 1)
        if found is not None:
            return found
    return None


def bfs(root: tuple[int, int], searched: (int, int), input_data: np.ndarray) -> int:
    queue, visited = deque(), set()
    queue.append([root])

    while queue:
        path = queue.popleft()
        row, col = path[-1]

        if (row, col) not in visited:
            visited.add((row, col))

            if (row, col) == searched:
                return len(path) - 1

            for height, vertex, delta in connected_neighbors(node=(row, col), grid=input_data):
                if delta <= 1:
                    path_copy = path[:]
                    path_copy.append(vertex)
                    queue.append(path_copy)


# sampled from Mahakaal https://github.com/mahakaal/adventofcode/blob/main/2022/day12/day12.py
def get_adjacent(current: (int, int), cols, rows) -> [(int, int)]:
    col, row = current

    match current:
        case (0, 0):
            return [(0, 1), (1, 0)]
        case (0, x):
            return [(col, row - 1), (col + 1, row)] if x == rows - 1 else [(col, row - 1), (col + 1, row),
                                                                           (col, row + 1)]
        case (y, 0):
            return [(col - 1, row), (col, row + 1)] if y == cols - 1 else [(col - 1, row), (col, row + 1),
                                                                           (col + 1, row)]
        case _:
            if current == (cols - 1, rows - 1):
                return [(col, row - 1), (col - 1, row)]
            elif col == cols - 1:
                return [(col, row - 1), (col - 1, row), (col, row + 1)]
            elif row == rows - 1:
                return [(col, row - 1), (col - 1, row), (col + 1, row)]
            else:
                return [(col, row - 1), (col - 1, row), (col, row + 1), (col + 1, row)]


def bfs2(root: (int, int), searched: (int, int), input_data: [[str]]) -> int:
    values = {chr(i): i - 96 for i in range(97, 97 + 26)}
    values['S'] = 1
    values['E'] = 26

    queue, visited = deque(), set()
    queue.append([root])

    while queue:
        path = queue.popleft()
        row, col = path[-1]
        current_height = values[input_data[row][col]]

        if (row, col) not in visited:
            visited.add((row, col))

            if (row, col) == searched:
                return len(path) - 1

            for vertex in get_adjacent((row, col), len(input_data), len(input_data[0])):
                vertex_row, vertex_col = vertex
                vertex_height = values[input_data[vertex_row][vertex_col]]

                if vertex_height <= current_height + 1:
                    path_copy = path[:]
                    path_copy.append(vertex)
                    queue.append(path_copy)


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

        # visited = set()
        # navigable_neighbors = plot_navigable_neighbors(heightmap)
        # dfs(visited=visited, graph=navigable_neighbors, node=end_coord, steps=0)
        answer = bfs(root=start_coord, searched=end_coord, input_data=heightmap)
        print(answer)

        starting, ending = None, None

        for r, line in enumerate(input_data):
            if 'S' in line:
                starting = (r, line.index('S'))

            if 'E' in line:
                ending = (r, line.index('E'))

        print(f"Part 1 - %d" % bfs2(starting, ending, input_data))
