"""
--- Day 16: Proboscidea Volcanium ---
The sensors have led you to the origin of the distress signal: yet another handheld device, just like the one the Elves gave you. However, you don't see any Elves around; instead, the device is surrounded by elephants! They must have gotten lost in these tunnels, and one of the elephants apparently figured out how to turn on the distress signal.

The ground rumbles again, much stronger this time. What kind of cave is this, exactly? You scan the cave with your handheld device; it reports mostly igneous rock, some ash, pockets of pressurized gas, magma... this isn't just a cave, it's a volcano!

You need to get the elephants out of here, quickly. Your device estimates that you have 30 minutes before the volcano erupts, so you don't have time to go back out the way you came in.

You scan the cave for other options and discover a network of pipes and pressure-release valves. You aren't sure how such a system got into a volcano, but you don't have time to complain; your device produces a report (your puzzle input) of each valve's flow rate if it were opened (in pressure per minute) and the tunnels you could use to move between the valves.

There's even a valve in the room you and the elephants are currently standing in labeled AA. You estimate it will take you one minute to open a single valve and one minute to follow any tunnel from one valve to another. What is the most pressure you could release?

For example, suppose you had the following scan output:

Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
All of the valves begin closed. You start at valve AA, but it must be damaged or jammed or something: its flow rate is 0, so there's no point in opening it. However, you could spend one minute moving to valve BB and another minute opening it; doing so would release pressure during the remaining 28 minutes at a flow rate of 13, a total eventual pressure release of 28 * 13 = 364. Then, you could spend your third minute moving to valve CC and your fourth minute opening it, providing an additional 26 minutes of eventual pressure release at a flow rate of 2, or 52 total pressure released by valve CC.

Making your way through the tunnels like this, you could probably open many or all of the valves by the time 30 minutes have elapsed. However, you need to release as much pressure as possible, so you'll need to be methodical. Instead, consider this approach:

== Minute 1 ==
No valves are open.
You move to valve DD.

== Minute 2 ==
No valves are open.
You open valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You move to valve CC.

== Minute 4 ==
Valve DD is open, releasing 20 pressure.
You move to valve BB.

== Minute 5 ==
Valve DD is open, releasing 20 pressure.
You open valve BB.

== Minute 6 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve AA.

== Minute 7 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve II.

== Minute 8 ==
Valves BB and DD are open, releasing 33 pressure.
You move to valve JJ.

== Minute 9 ==
Valves BB and DD are open, releasing 33 pressure.
You open valve JJ.

== Minute 10 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve II.

== Minute 11 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve AA.

== Minute 12 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve DD.

== Minute 13 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve EE.

== Minute 14 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve FF.

== Minute 15 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve GG.

== Minute 16 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You move to valve HH.

== Minute 17 ==
Valves BB, DD, and JJ are open, releasing 54 pressure.
You open valve HH.

== Minute 18 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve GG.

== Minute 19 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve FF.

== Minute 20 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve EE.

== Minute 21 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve EE.

== Minute 22 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve DD.

== Minute 23 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You move to valve CC.

== Minute 24 ==
Valves BB, DD, EE, HH, and JJ are open, releasing 79 pressure.
You open valve CC.

== Minute 25 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 27 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 28 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 29 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

== Minute 30 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
This approach lets you release the most pressure possible in 30 minutes with this valve layout, 1651.

Work out the steps to release the most pressure in 30 minutes. What is the most pressure you can release?
"""

from collections import deque
from dataclasses import dataclass, field
from itertools import permutations
import re


@dataclass
class Valve:
    name: str
    flow_rate: int
    neighbors: dict[str, 'Valve'] = field(init=False)


def parse_input(file_path: str):
    valves = {}
    neighbors = {}
    with open(file_path) as f:
        for line in f:
            valve_id = line[6:8]
            flow_rate = int(re.findall(r'(?!=)\d+', line)[0])
            valves[valve_id] = Valve(name=valve_id, flow_rate=flow_rate)
            neighbors[valve_id] = re.findall(r'[A-Z]{2}', line)[1:]
        for valve, connections in neighbors.items():
            valves[valve].neighbors = {c: valves[c] for c in connections}
    return valves


# https://nbviewer.org/github/mjpieters/adventofcode/blob/master/2022/Day%2016.ipynb
def get_distances(graph: dict[str, Valve]) -> dict[str, dict[str, int]]:
    """
    Uses the Floyd-Warshall algorithm to find the minimum distances from any node in the graph to
    any other node.
    :param graph:
    :return:
    """
    # set dist of 1 for nearest neighboring nodes
    dist = {v: {n: 1 for n in graph[v].neighbors} for v in graph}
    # assume maximum distance to visit another node is to vist every node in the graph
    max_dist = len(graph)
    # plot distance to all nodes from any given node by finding the minimum distance through
    # given permutation intermediary
    for k, i, j in permutations(graph, r=3):
        try:
            dist[i][j] = min(dist[i][k] + dist[k][j], dist[i].get(j, max_dist))
        except KeyError:
            # A node hasn't been plotted yet in the dictionary as connected, but will eventually
            # since all permutations will be attempted
            pass
    return dist


@dataclass
class PressureReliefPath:
    valve: str
    time_left: int = 30
    total_released: int = 0
    visited: frozenset[str] = frozenset()

    def traverse(self, distances: dict[str, dict[str, int]], valves: dict[str, Valve]):
        for valve, steps in distances[self.valve].items():
            if valve in self.visited or valves[valve].flow_rate == 0:
                # either valve has been visited or it has no potential pressure relief possible
                continue
            if (time_left := self.time_left - steps - 1) <= 0:
                # Insufficient time remaining to visit the valve and make an impact
                continue
            yield __class__(
                valve,
                time_left,
                self.total_released + valves[valve].flow_rate * time_left,
                self.visited | {valve}
            )


def max_pressure_relief(remaining: int, distances: dict[str, dict[str, int]], valves: dict[str, Valve]):
    max_relief = {}
    queue = deque([PressureReliefPath(valve='AA', time_left=remaining)])
    while queue:
        node = queue.popleft()
        for new in node.traverse(distances=distances, valves=valves):
            max_relief[new.visited] = max(max_relief.get(new.visited, 0), new.total_released)
            queue.append(new)
    return max_relief


# def bfs(root: str, end_node: str, valves: dict[str, Valve]):  # -> int:
#     queue, visited = deque(), set()
#     queue.append([root])
#
#     while queue:
#         path = queue.popleft()
#         valve = path[-1]
#
#         if valve not in visited:
#             visited.add(valve)
#
#             # if valve == end_node:
#             #     return len(path) - 1
#
#             for neighbor_valve in valves[valve].neighbors:
#                 path_copy = path[:]
#                 path_copy.append(neighbor_valve)
#                 queue.append(path_copy)
#                 print(queue)
#     print(visited)
#
#
# def dfs(visited: dict,
#         graph: dict[str, Valve],
#         node: str,
#         steps: int = 0):
#     if node not in visited:
#         visited[node] = steps
#         for neighbor in graph[node].neighbors:
#             visited.update(dfs(visited=visited, graph=graph, node=neighbor, steps=steps + 1))
#     return visited


if __name__ == '__main__':
    valves = parse_input('input.txt')
    # results = dfs(visited={}, graph=valves, node='AA', steps=0)
    # results2 = bfs('AA', 'JJ', valves)
    # non_zero_valves = []
    dist = get_distances(graph=valves)
    max_reliefs = max_pressure_relief(remaining=30, distances=dist, valves=valves)
    print(max(max_reliefs.values()))
