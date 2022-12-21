

if __name__ == '__main__':
    with open('input.csv', 'r') as f:
        elf_num = 1
        elf_sum = 0
        max = 0
        for line in f:
            if line == '\n':
                elf_num += 1
                if elf_sum > max:
                    max = elf_sum
                elf_sum = 0
            else:
                elf_sum += int(line.strip())
        print(max)
