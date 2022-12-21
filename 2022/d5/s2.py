"""
--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   d3
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   d3
However, the action of moving three crates from stack 1 to stack d3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   d3
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   d3
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   d3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?
"""
from queue import LifoQueue, Queue
from s1 import read_header


def move_crate(dock: dict[int: LifoQueue], start: int, end: int, quantity: int):
    temp = LifoQueue()
    for _ in range(quantity):
        temp.put(dock[start].get())
    for _ in range(quantity):
        dock[end].put(temp.get())


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        dock = read_header(f)
        for line in f:
            instructions = line.split()
            # for _ in range(int(instructions[1])):
            move_crate(dock=dock,
                       start=int(instructions[3]),
                       end=int(instructions[5]),
                       quantity=int(instructions[1]))
        print(''.join(dock[stack].get() for stack in dock))
