"""
--- Part Two ---
Your handheld device indicates that the distress signal is coming from a beacon nearby. The distress beacon is not detected by any sensor, but the distress beacon must have x and y coordinates each no lower than 0 and no larger than 4000000.

To isolate the distress beacon's signal, you need to determine its tuning frequency, which can be found by multiplying its x coordinate by 4000000 and then adding its y coordinate.

In the example above, the search space is smaller: instead, the x and y coordinates can each be at most 20. With this reduced search area, there is only a single position that could have a beacon: x=14, y=11. The tuning frequency for this distress beacon is 56000011.

Find the only possible position for the distress beacon. What is its tuning frequency?
"""
from s1 import parse_input, spans_covering_row


def find_uncovered(spans: list[tuple[int, int]]):
    # assumes there is only 1 uncovered space
    right = spans[0][1]
    found = False
    found_pos = None
    for span in spans:
        if right > span[0] and right >= span[1]:
            continue
        elif right < span[0] - 1:
            # print(span, right)
            found = True
            found_pos = right + 1
        elif right < span[1]:
            right = span[1]
    return found, found_pos


if __name__ == '__main__':
    sensors, _ = parse_input('input.txt')
    boundaries = (0, 4000000)
    for row_to_check in range(boundaries[0], boundaries[1] + 1):
        covered_spans = spans_covering_row(sensors=sensors,
                                           row=row_to_check)
        any_uncovered, position = find_uncovered(spans=covered_spans)
        if any_uncovered:
            print((position * 4000000) + row_to_check)
