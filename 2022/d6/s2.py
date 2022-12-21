"""
--- Part Two ---
Your device's communication system is correctly detecting packets, but still isn't working. It looks like it also needs to look for messages.

A start-of-message marker is just like a start-of-packet marker, except it consists of 14 distinct characters rather than 4.

Here are the first positions of start-of-message markers for all of the above examples:

mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
How many characters need to be processed before the first start-of-message marker is detected?
"""


from s1 import get_uniques

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        line = f.readline()
        start = line[:14]
        if len(get_uniques(start)) == 14:
            print(4)
        else:
            for x in range(1, len(line)-13):
                if len(get_uniques(line[x:x+14])) == 14:
                    print(x+14)
                    break
