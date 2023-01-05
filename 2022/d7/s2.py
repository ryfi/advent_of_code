"""
--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
"""

from s1 import Directory, map_hard_drive


def smaller_dif(min_deletion_needed: int, current_min_size: int, new_drive_size: int) -> int:
    dif_new = min_deletion_needed - new_drive_size
    if dif_new > 0:
        return current_min_size
    dif_current = min_deletion_needed - current_min_size
    if dif_current > 0:
        return new_drive_size
    if abs(dif_current) < abs(dif_new):
        return current_min_size
    else:
        return new_drive_size


def find_min_iter(directory: Directory, min_deletion_needed: int, current_min_found: int) -> int:
    stack = [directory]
    while stack:
        top = stack.pop()
        for _, sub_dir in top.subdirectories.items():
            stack.append(sub_dir)
        current_min_found = smaller_dif(min_deletion_needed=min_deletion_needed,
                                        current_min_size=current_min_found,
                                        new_drive_size=top.size)
    return current_min_found


if __name__ == '__main__':
    hd = map_hard_drive('input.txt')
    hd_max_space = 70000000
    min_space_needed = 30000000
    unused_space = hd_max_space - hd.total_size()
    min_deletion_needed = min_space_needed - unused_space
    # print(hd.size)
    # print(f'{unused_space=}, {hd_max_space=}, {min_deletion_needed=}')
    print(find_min_iter(directory=hd,
                        min_deletion_needed=min_deletion_needed,
                        current_min_found=hd.size))
