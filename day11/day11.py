"""
The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
--- Part Two ---
The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
"""
import sys
from collections import deque, defaultdict
import heapq


def solve():
    factor = 1000000
    matrix = [list(line.strip()) for line in input]
    # expand the universe
    rows_to_expand = set()
    cols_to_expand = set()
    m, n = len(matrix), len(matrix[0])
    for i in range(m):
        if "#" not in matrix[i]:
            rows_to_expand.add(i)
    for j in range(n):
        if "#" not in [matrix[i][j] for i in range(m)]:
            cols_to_expand.add(j)
    label = 0
    galaxies = set()
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == "#":
                matrix[i][j] = str(label)
                label += 1
                galaxies.add((i, j))
    # new_matrix = []
    # for i in range(m):
    #     new_matrix.append(matrix[i].copy())
    #     if i in rows_to_expand:
    #         new_matrix.append(matrix[i].copy())
    # matrix = [line.copy() for line in new_matrix]
    # # for line in matrix:
    # #     print("".join(line))
    # new_matrix = [[] for _ in range(len(matrix))]
    # for j in range(n):
    #     for i in range(len(new_matrix)):
    #         new_matrix[i].append(matrix[i][j])
    #         if j in cols_to_expand:
    #             new_matrix[i].append(matrix[i][j])
    # matrix = [line.copy() for line in new_matrix]
    for line in matrix:
        print("".join(line))
    m, n = len(matrix), len(matrix[0])

    # def bfs(i, j):
    #     visited = set([(i, j)])
    #     queue = deque([(i, j, 0)])
    #     res = 0
    #     while queue:
    #         i, j, dist = queue.popleft()
    #         if matrix[i][j] == "#":
    #             res += dist
    #         for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
    #             ni, nj = i + di, j + dj
    #             if (
    #                 0 <= ni < len(matrix)
    #                 and 0 <= nj < len(matrix[0])
    #                 and (ni, nj) not in visited
    #             ):
    #                 queue.append((ni, nj, dist + 1))
    #                 visited.add((ni, nj))
    #     return res
    labels = set([str(i) for i in range(label)])

    def djkstra(i, j):
        # Initialize distances as infinite and the start node distance as 0
        distances = defaultdict(lambda: float("inf"))
        start = (i, j)
        distances[start] = 0

        # Initialize the priority queue and add the start node
        priority_queue = [(0, start)]

        while priority_queue:
            # print(priority_queue)
            current_distance, current_node = heapq.heappop(priority_queue)

            # Consider next unvisited node with the smallest known distance
            if current_distance > distances[current_node]:
                continue
            i, j = current_node
            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                ni, nj = i + di, j + dj
                if ni < 0 or ni >= m or nj < 0 or nj >= n:
                    continue
                neighbor = (ni, nj)
                weight = 1
                if (di, dj) in [(1, 0), (-1, 0)] and ni in rows_to_expand:
                    weight *= factor
                if (di, dj) in [(0, 1), (0, -1)] and nj in cols_to_expand:
                    weight *= factor
                distance = current_distance + weight
                # print(distance, neighbor, distances[neighbor])
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        # print(distances)
        return sum(distances[(i, j)] for i, j in galaxies)

    res = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] in labels:
                res += djkstra(i, j)
    print(res, res // 2)


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve()
