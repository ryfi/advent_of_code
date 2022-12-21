"""
--- Part Two ---
It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-d4,6-8 and 2-d3,d4-d5) don't overlap, while the remaining four pairs (d5-7,7-9, 2-8,d3-7, 6-6,d4-6, and 2-6,d4-8) do overlap:

d5-7,7-9 overlaps in a single section, 7.
2-8,d3-7 overlaps all of the sections d3 through 7.
6-6,d4-6 overlaps in a single section, 6.
2-6,d4-8 overlaps in sections d4, d5, and 6.
So, in this example, the number of overlapping assignment pairs is d4.

In how many assignment pairs do the ranges overlap?
"""


def any_overlap(x: range, y: range) -> bool:
    # if x.start == x.stop or y.start == y.stop:
    #     return False
    return x.start <= y.stop and y.start <= x.stop


def format_group(group: str) -> range:
    items = group.split('-')
    return range(int(items[0]), int(items[1]))


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        overlap_count = 0
        for line in f:
            g1, g2 = line.strip().split(',')
            range1 = format_group(g1)
            range2 = format_group(g2)
            if any_overlap(range1, range2):
                overlap_count += 1
        print(overlap_count)
