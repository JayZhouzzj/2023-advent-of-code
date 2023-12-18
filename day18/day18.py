"""
However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?
"""
import sys
from collections import defaultdict
import heapq


def solve():
    curr = [0, 0]
    border = set()
    border.add(tuple(curr))
    dir_to_offset = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for line in input:
        line = line.strip().split()
        direction = line[0]
        distance = int(line[1])
        for _ in range(distance):
            curr[0] += dir_to_offset[direction][0]
            curr[1] += dir_to_offset[direction][1]
            min_x = min(min_x, curr[0])
            min_y = min(min_y, curr[1])
            max_x = max(max_x, curr[0])
            max_y = max(max_y, curr[1])
            border.add(tuple(curr))
    inside_count = 0
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            meet = 0
            if (i, j) not in border:
                next_i, next_j = i, j
                while next_i <= max_x and next_j <= max_y:
                    if (
                        (next_i, next_j) in border
                        and (
                            not (
                                (next_i, next_j - 1) in border
                                and (next_i + 1, next_j) in border
                            )
                        )
                        and (
                            not (
                                (next_i, next_j + 1) in border
                                and (next_i - 1, next_j) in border
                            )
                        )
                    ):
                        meet += 1
                    next_i += 1
                    next_j += 1
                if meet % 2 == 1:
                    inside_count += 1
    print(len(border), inside_count, len(border) + inside_count)


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve()
