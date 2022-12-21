from queue import PriorityQueue

if __name__ == '__main__':
    with open('input.csv', 'r') as f:
        elf_num = 1
        elf_sum = 0
        max_sums = PriorityQueue(3)
        for line in f:
            if line == '\n':
                elf_num += 1
                if max_sums.full():
                    lowest_max = max_sums.get()
                    if elf_sum > lowest_max:
                        max_sums.put(elf_sum)
                    else:
                        max_sums.put(lowest_max)
                else:
                    max_sums.put(elf_sum)
                elf_sum = 0
            else:
                elf_sum += int(line.strip())
        l = [max_sums.get() for _ in range(max_sums.qsize())]
        print(l)
        print(sum(l))
