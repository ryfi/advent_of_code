"""
--- Day d5: Supply Stacks ---
The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   d3

move 1 from 2 to 1
move d3 from 1 to d3
move 2 from 2 to 1
move 1 from 1 to 2
In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack d3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]
[N] [C]
[Z] [M] [P]
 1   2   d3
In the second step, three crates are moved from stack 1 to stack d3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   d3
Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   d3
Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   d3
The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack d3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?
"""
from io import TextIOWrapper
from queue import LifoQueue


def read_header(f: TextIOWrapper):
    previous_line = f.readline()
    raw_stack_rows: list[str] = [previous_line]
    stacks: list[str] = []
    dock: dict[int: LifoQueue] = {}
    for line in f:
        if line == '\n':
            stacks: list[str] = raw_stack_rows.pop().split()
            dock = {int(stack): LifoQueue() for stack in stacks}
            break
        else:
            raw_stack_rows.append(line)
            previous_line = line
    # print(dock, raw_stack_rows)
    for line in raw_stack_rows[::-1]:
        crates = [line[x] for x in range(1, len(line), 4)]
        for crate_pos in range(len(dock)):
            if crates[crate_pos] == ' ':
                pass
            else:
                dock[crate_pos + 1].put(crates[crate_pos])
    return dock


def move_crate(dock: dict[int: LifoQueue], start: int, end: int):
    dock[end].put(dock[start].get())


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        dock = read_header(f)
        for line in f:
            instructions = line.split()
            for _ in range(int(instructions[1])):
                move_crate(dock, int(instructions[3]), int(instructions[5]))
        print(''.join(dock[stack].get() for stack in dock))

