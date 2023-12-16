"""
Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?
--- Part Two ---
As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?
"""
import sys
from collections import deque


def solve():
    # bfs
    matrix = [list(line.strip()) for line in input]
    m = len(matrix)
    n = len(matrix[0])

    def append_next(next, curr_dir):
        next_i, next_j = next
        if matrix[next_i][next_j] == ".":
            q.append((next, curr_dir))
        elif matrix[next_i][next_j] == "/":
            if curr_dir == "right":
                q.append((next, "up"))
            elif curr_dir == "left":
                q.append((next, "down"))
            elif curr_dir == "up":
                q.append((next, "right"))
            elif curr_dir == "down":
                q.append((next, "left"))
        elif matrix[next_i][next_j] == "\\":
            if curr_dir == "right":
                q.append((next, "down"))
            elif curr_dir == "left":
                q.append((next, "up"))
            elif curr_dir == "up":
                q.append((next, "left"))
            elif curr_dir == "down":
                q.append((next, "right"))
        elif matrix[next_i][next_j] == "|":
            if curr_dir == "right" or curr_dir == "left":
                q.append((next, "up"))
                q.append((next, "down"))
            else:
                q.append((next, curr_dir))
        elif matrix[next_i][next_j] == "-":
            if curr_dir == "up" or curr_dir == "down":
                q.append((next, "left"))
                q.append((next, "right"))
            else:
                q.append((next, curr_dir))

    start = (0, 0)
    visited = set()
    # visited.add((start, "right"))
    q = deque()
    append_next(start, "right")
    while q:
        curr = q.popleft()
        if curr in visited:
            continue
        visited.add(curr)
        if curr[1] == "right":
            next = (curr[0][0], curr[0][1] + 1)
        elif curr[1] == "left":
            next = (curr[0][0], curr[0][1] - 1)
        elif curr[1] == "up":
            next = (curr[0][0] - 1, curr[0][1])
        elif curr[1] == "down":
            next = (curr[0][0] + 1, curr[0][1])
        next_i, next_j = next
        if next_i < 0 or next_i >= m or next_j < 0 or next_j >= n:
            continue
        append_next(next, curr[1])
    visited_cells = set([(x, y) for (x, y), _ in visited])
    # print(visited_cells)
    for i in range(m):
        for j in range(n):
            if (i, j) in visited_cells:
                matrix[i][j] = "#"
            else:
                matrix[i][j] = "."
    for line in matrix:
        print("".join(line))
    print(len(visited_cells))


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve()
