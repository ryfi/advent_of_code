"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
"""

from dataclasses import dataclass, field

from typing import List


@dataclass
class File:
    name: str = ''
    size: int = 0


@dataclass
class Directory(File):
    # name: str = ''
    # size: int = 0
    files: list[File] = field(default_factory=list)
    subdirectories: dict[str, 'Directory'] = field(default_factory=dict)

    def __iter__(self):
        for _, sub_dir in self.subdirectories.items():
            yield sub_dir

    def _update_total_size(self):
        self.size = sum([file.size for file in self.files if file is not None]) + \
                    sum([self.subdirectories[subdir].total_size() for subdir in self.subdirectories])

    def total_size(self) -> int:
        # total = sum([file.size for file in self.files if file is not None]) + \
        #         sum([subdir.total_size() for subdir in self.subdirectories if subdir is not None])
        # self.size = total
        self._update_total_size()
        return self.size

    def sum_size_under(self, max_size: int):

        file_sum = 0
        dir_sum = 0
        for file in self.files:
            if file.size < max_size:
                file_sum += file.size
        for directory in self.subdirectories:
            subdir_sum = self.subdirectories[directory].total_size()
            if subdir_sum < max_size:
                dir_sum += subdir_sum
        if self.size < max_size:
            dir_sum += self.size
        return file_sum + dir_sum


def get_from_directory(hd: Directory, pwd_list: list) -> Directory:
    if len(pwd_list) == 1:
        return hd.subdirectories[pwd_list[0]]
    else:
        return get_from_directory(hd=hd.subdirectories[pwd_list[0]],
                                  pwd_list=pwd_list[1:])


def sum_size_under(hd: Directory, max_size: int) -> int:
    hd.total_size()
    total = 0
    if len(hd.subdirectories) > 0:
        for _, sub_dir in hd.subdirectories.items():
            total += sum_size_under(hd=sub_dir, max_size=max_size)
    if hd.size < max_size:
        total += hd.size
    return total


def map_hard_drive(f_path) -> Directory:
    with open(f_path, 'r') as f:
        _ = f.readline()
        hd = Directory(name='hard_drive', subdirectories={'/': Directory(name='/')})
        pwd = ['/']
        for line in f:
            match line.split():
                case ['$', 'cd', '/']:
                    # root
                    pwd = ['/']
                case ['$', 'cd', '..']:
                    # moved up
                    pwd.pop()
                case ['$', 'cd', x]:
                    pwd.append(x)
                case ['$', 'ls']:
                    # listing content
                    pass
                case ['dir', dir_name]:
                    current_dir = get_from_directory(hd, pwd)
                    current_dir.subdirectories[dir_name] = Directory(name=dir_name)
                case [file_size, file_name]:
                    current_dir = get_from_directory(hd, pwd)
                    current_dir.files.append(File(name=file_name, size=int(file_size)))
    return hd


if __name__ == '__main__':
    hd = map_hard_drive('input.txt')
    print(sum_size_under(hd, 100000))
