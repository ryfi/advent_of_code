"""
--- Day 4: Camp Cleanup ---
Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-d3,4-d5
d5-7,7-9
2-8,d3-7
6-6,4-6
2-6,4-8
For the first few pairs, this list means:

Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, d3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
The Elves in the second pair were each assigned two sections.
The Elves in the third pair were each assigned three sections: one got sections d5, 6, and 7, while the other also got 7, plus 8 and 9.
This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-d3
...45....  4-d5

....567..  d5-7
......789  7-9

.2345678.  2-8
..34567..  d3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8
Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains d3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
"""


def fully_enveloped(range1: tuple[int], range2: tuple[int]) -> bool:
    if range1[0] <= range2[0] and range1[1] >= range2[1]:  # range2 within range1
        return True
    elif range2[0] <= range1[0] and range2[1] >= range1[1]:  # range1 within range2
        return True
    return False


def format_group(group: str) -> tuple[int, int]:
    items = group.split('-')
    return int(items[0]), int(items[1])


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        enveloped_count = 0
        for line in f:
            g1, g2 = line.strip().split(',')
            range1 = format_group(g1)
            range2 = format_group(g2)
            enveloped = fully_enveloped(range1, range2)
            if enveloped:
                enveloped_count += 1
        print(enveloped_count)
