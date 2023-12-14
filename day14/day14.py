"""
In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?
"""
import sys
from functools import cache


def roll(matrix):
    # print(matrix)
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            if matrix[i][j] == "O":
                while i - 1 >= 0 and matrix[i - 1][j] == ".":
                    matrix[i][j], matrix[i - 1][j] = matrix[i - 1][j], matrix[i][j]
                    i -= 1
    # print("N")
    # for line in matrix:
    #     print("".join(line))
    # print()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == "O":
                while j - 1 >= 0 and matrix[i][j - 1] == ".":
                    matrix[i][j], matrix[i][j - 1] = matrix[i][j - 1], matrix[i][j]
                    j -= 1
    # print("W")
    # for line in matrix:
    #     print("".join(line))
    # print()
    for j in range(len(matrix[0])):
        for i in range(len(matrix) - 1, -1, -1):
            if matrix[i][j] == "O":
                while i + 1 < len(matrix) and matrix[i + 1][j] == ".":
                    matrix[i][j], matrix[i + 1][j] = matrix[i + 1][j], matrix[i][j]
                    i += 1
    # print("S")
    # for line in matrix:
    #     print("".join(line))
    # print()
    for i in range(len(matrix)):
        for j in range(len(matrix[0]) - 1, -1, -1):
            if matrix[i][j] == "O":
                while j + 1 < len(matrix[0]) and matrix[i][j + 1] == ".":
                    matrix[i][j], matrix[i][j + 1] = matrix[i][j + 1], matrix[i][j]
                    j += 1
    # print("E")
    # for line in matrix:
    #     print("".join(line))
    # print()


def solve():
    matrix = [list(line.strip()) for line in input]
    seen = {}
    idx_to_matrix = {}
    start, end = None, None
    for i in range(1000000000):
        roll(matrix)
        t_matrix = tuple(tuple(line) for line in matrix)
        idx_to_matrix[i] = t_matrix
        if t_matrix in seen:
            start, end = seen[t_matrix], i
            break
        seen[t_matrix] = i
    offset = (1000000000 - 1 - start) % (end - start)
    print(start, end, start + offset)
    res = sum(
        [
            (len(matrix) + 1 - i) * line.count("O")
            for i, line in enumerate(idx_to_matrix[start + offset], 1)
        ]
    )
    print(res)


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve()
