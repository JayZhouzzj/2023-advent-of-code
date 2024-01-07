"""
ue to strong, probably-magical winds, the hailstones are all flying through the air in perfectly linear trajectories. You make a note of each hailstone's position and velocity (your puzzle input). For example:

19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
Each line of text corresponds to the position and velocity of a single hailstone. The positions indicate where the hailstones are right now (at time 0). The velocities are constant and indicate exactly how far each hailstone will move in one nanosecond.

Each line of text uses the format px py pz @ vx vy vz. For instance, the hailstone specified by 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y position 19, Z position 15, X velocity 1, Y velocity -5, and Z velocity -3. After one nanosecond, the hailstone would be at 21, 14, 12.

Perhaps you won't have to do anything. How likely are the hailstones to collide with each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward in time, how many of the hailstones' paths will intersect within a test area? (The hailstones themselves don't have to collide, just test for intersections between the paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at least 7 and at most 27; in your actual data, you'll need to check a much larger test area. Comparing all pairs of hailstones' future paths produces the following results:

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
So, in this example, 2 hailstones' future paths cross inside the boundaries of the test area.

However, you'll need to search a much larger test area if you want to see if any hailstones might collide. Look for intersections that happen with an X and Y position each at least 200000000000000 and at most 400000000000000. Disregard the Z axis entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections. How many of these intersections occur within the test area?
"""
import sys


def parse_input(input_data):
    hailstones = []
    for line in input_data:
        parts = line.split(" @ ")
        position = tuple(map(int, parts[0].split(", ")))
        velocity = tuple(map(int, parts[1].split(", ")))
        hailstones.append((position, velocity))
    return hailstones


def compute_intersection(px_a, py_a, vx_a, vy_a, px_b, py_b, vx_b, vy_b):
    # Check for parallel lines (slopes are equal)
    if vx_a * vy_b == vy_a * vx_b:
        return None  # Lines are parallel or coincident, no unique intersection

    # Calculate the intersection point
    x = ((vy_a / vx_a) * px_a - (vy_b / vx_b) * px_b + py_b - py_a) / (
        (vy_a / vx_a) - (vy_b / vx_b)
    )
    y = (vy_a / vx_a) * (x - px_a) + py_a
    # print(x, y)
    return x, y


def find_intersection(h1, h2, test_area):
    (px_a, py_a, _), (vx_a, vy_a, _) = h1
    (px_b, py_b, _), (vx_b, vy_b, _) = h2

    intersection = compute_intersection(px_a, py_a, vx_a, vy_a, px_b, py_b, vx_b, vy_b)
    if intersection is None:
        return False
    return (
        test_area[0] <= intersection[0] <= test_area[1]
        and test_area[0] <= intersection[1] <= test_area[1]
        and ((intersection[0] - px_a) * vx_a) >= 0
        and ((intersection[0] - px_b) * vx_b) >= 0
    )


def count_intersections(hailstones, test_area):
    count = 0
    n = len(hailstones)
    for i in range(n):
        for j in range(i + 1, n):
            if find_intersection(hailstones[i], hailstones[j], test_area):
                count += 1
    return count


def solve():
    hailstones = parse_input(input)
    test_area = (200000000000000, 400000000000000)
    print(count_intersections(hailstones, test_area))


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve()
