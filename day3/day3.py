"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.
"""

import sys
from collections import defaultdict

nums = {}
gear_to_nums = defaultdict(set)


def solve(input):
    sum = 0
    matrix = []
    for line in input:
        line = line.strip()
        matrix.append(line)
    m = len(matrix)
    n = len(matrix[0])

    def update_gear(i, j, numi, numj):
        if i in range(m) and j in range(n) and matrix[i][j] == "*":
            gear_to_nums[(i, j)].add((numi, numj))

    def get(i, j):
        num = 0
        good = False
        col = j
        while col < n and matrix[i][col].isdigit():
            num = num * 10 + int(matrix[i][col])

            update_gear(i - 1, col, i, j)
            update_gear(i + 1, col, i, j)
            update_gear(i, col - 1, i, j)
            update_gear(i, col + 1, i, j)
            update_gear(i - 1, col - 1, i, j)
            update_gear(i - 1, col + 1, i, j)
            update_gear(i + 1, col - 1, i, j)
            update_gear(i + 1, col + 1, i, j)

            col += 1
        nums[(i, j)] = num
        return num, col

    res = 0
    for i in range(m):
        j = 0
        while j < n:
            if not matrix[i][j].isdigit():
                j += 1
                continue
            num, col = get(i, j)
            j = col

    for gear in gear_to_nums:
        if len(gear_to_nums[gear]) == 2:
            num1, num2 = gear_to_nums[gear]
            res += nums[num1] * nums[num2]
            print(gear, gear_to_nums[gear], nums[num1], nums[num2])
    print(res)
    return res


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve(input)
