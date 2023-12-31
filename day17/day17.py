"""
Fortunately, the Elves here have a map (your puzzle input) that uses traffic patterns, ambient temperature, and hundreds of other parameters to calculate exactly how much heat loss can be expected for a crucible entering any particular city block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
Each city block is marked by a single digit that represents the amount of heat loss if the crucible enters that block. The starting point, the lava pool, is the top-left city block; the destination, the machine parts factory, is the bottom-right city block. (Because you already start in the top-left block, you don't incur that block's heat loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight line for very long, it can move at most three blocks in a single direction before it must turn 90 degrees left or right. The crucible also can't reverse direction; after entering each city block, it may only turn left, continue straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>
This path never moves more than three consecutive blocks in the same direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory, but not moving more than three consecutive blocks in the same direction, what is the least heat loss it can incur?
--- Part Two ---
The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the machine parts factory. Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in that direction before it can turn (or even before it can stop at the end). However, it will eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
In the above example, an ultra crucible would incur the minimum possible heat loss of 94.

Here's another example:

111111111111
999999999991
999999999991
999999999991
999999999991
Sadly, an ultra crucible would need to take an unfortunate path like this one:

1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, what is the least heat loss it can incur?
"""
import sys
from collections import defaultdict
import heapq


def solve():
    matrix = [[int(x) for x in list(line.strip())] for line in input]
    # print(matrix)
    m, n = len(matrix), len(matrix[0])
    # up, right, down, left
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def djkstra(i, j, dir, remain):
        # Initialize distances as infinite and the start node distance as 0
        distances = defaultdict(lambda: float("inf"))
        start = (i, j, dir, remain)
        distances[start] = 0

        # Initialize the priority queue and add the start node
        priority_queue = [(0, start)]

        while priority_queue:
            # print(priority_queue)
            current_distance, current_node = heapq.heappop(priority_queue)

            # Consider next unvisited node with the smallest known distance
            if current_distance > distances[current_node]:
                continue
            i, j, dir, remain = current_node
            candidates = [
                [dir, remain - 1],
            ]
            if remain <= 6:
                candidates += [
                    [(dir + 1) % 4, 9],
                    [(dir - 1) % 4, 9],
                ]
            for new_dir, new_remain in candidates:
                if new_remain < 0:
                    continue
                ni, nj = i + dirs[new_dir][0], j + dirs[new_dir][1]
                if ni < 0 or ni >= m or nj < 0 or nj >= n:
                    continue
                neighbor = (ni, nj, new_dir, new_remain)
                weight = matrix[ni][nj]
                distance = current_distance + weight
                # print(distance, neighbor, distances[neighbor])
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        # print(distances)
        return min(
            distances[(m - 1, n - 1, dir, remain)]
            for dir in range(4)
            for remain in range(7)
        )

    # for dir in range(4):
    #     print(djkstra(0, 0, dir, 3))
    print(min([djkstra(0, 0, dir, 10) for dir in range(4)]))


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve()
