"""
--- Part Two ---
Now, you just need to put all of the packets in the right order. Disregard the blank lines in your list of received packets.

The distress signal protocol also requires that you include two additional divider packets:

[[2]]
[[6]]
Using the same rules as before, organize all packets - the ones in your list of received packets as well as the two divider packets - into the correct order.

For the example above, the result of putting the packets in the correct order is:

[]
[[]]
[[[]]]
[1,1,3,1,1]
[1,1,5,1,1]
[[1],[2,3,4]]
[1,[2,[3,[4,[5,6,0]]]],8,9]
[1,[2,[3,[4,[5,6,7]]]],8,9]
[[1],4]
[[2]]
[3]
[[4,4],4,4]
[[4,4],4,4,4]
[[6]]
[7,7,7]
[7,7,7,7]
[[8,7,6]]
[9]
Afterward, locate the divider packets. To find the decoder key for this distress signal, you need to determine the indices of the two divider packets and multiply them together. (The first packet is at index 1, the second packet is at index 2, and so on.) In this example, the divider packets are 10th and 14th, and so the decoder key is 140.

Organize all of the packets into the correct order. What is the decoder key for the distress signal?
"""

from json import loads as convert_input
from s1 import iterate_packet_list


def parse_input(file_path: str):
    all_data = []
    with open(file_path) as f:
        for line in f:
            if line == '\n':
                continue
            else:
                all_data.append(convert_input(line.strip()))
    return all_data


if __name__ == '__main__':
    packet_data = parse_input('input.txt')
    packet_data.append([[2]])
    packet_data.append([[6]])

    correct_order_count = 0
    order_is_correct = False
    while not order_is_correct:
        for packet_idx in range(len(packet_data) - 1):
            left_packet = packet_data[packet_idx]
            right_packet = packet_data[packet_idx + 1]
            for operation, left, right in iterate_packet_list(left_packet, right_packet):
                if operation == 'correct':
                    correct_order_count += 1
                    break
                elif operation == 'disordered':
                    packet_data[packet_idx], packet_data[packet_idx + 1] = \
                        packet_data[packet_idx + 1], packet_data[packet_idx]
                    break
                elif left < right:
                    # Left side is smaller, so inputs are in the right order
                    correct_order_count += 1
                    break
                elif right < left:
                    # Right side is smaller, so inputs are not in the right order
                    packet_data[packet_idx], packet_data[packet_idx + 1] = \
                        packet_data[packet_idx + 1], packet_data[packet_idx]
                    break
                elif left == right:
                    continue
        if correct_order_count >= len(packet_data) - 1:
            order_is_correct = True
        else:
            correct_order_count = 0
    print((packet_data.index([[2]]) + 1) * (packet_data.index([[6]]) + 1))
