"""
As you reach the bottom of the relentless avalanche of machine parts, you discover that they're already forming a formidable heap. Don't worry, though - a group of Elves is already here organizing the parts, and they have a system.

To start, each part is rated in each of four categories:

x: Extremely cool looking
m: Musical (it makes a noise when you hit it)
a: Aerodynamic
s: Shiny
Then, each part is sent through a series of workflows that will ultimately accept or reject the part. Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is true. The first rule that matches the part being considered is applied immediately, and the part moves on to the destination described by the rule. (The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow ex{x>10:one,m<20:two,a>30:R,A}. This workflow is named ex and contains four rules. If workflow ex were considering a specific part, it would perform the following steps in order:

Rule "x>10:one": If the part's x is more than 10, send the part to the workflow named one.
Rule "m<20:two": Otherwise, if the part's m is less than 20, send the part to the workflow named two.
Rule "a>30:R": Otherwise, if the part's a is more than 30, the part is immediately rejected (R).
Rule "A": Otherwise, because no other rules matched the part, the part is immediately accepted (A).
If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns. If a part is accepted (sent to A) or rejected (sent to R), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes. The Elves ask if you can help sort a few parts and give you the list of workflows and some part ratings (your puzzle input). For example:

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort. All parts begin in the workflow named in. In this example, the five listed parts go through the following workflows:

{x=787,m=2655,a=1222,s=2876}: in -> qqz -> qs -> lnx -> A
{x=1679,m=44,a=2067,s=496}: in -> px -> rfg -> gd -> R
{x=2036,m=264,a=79,s=2244}: in -> qqz -> hdj -> pv -> A
{x=2461,m=1339,a=466,s=291}: in -> px -> qkq -> crn -> R
{x=2127,m=1623,a=2188,s=1013}: in -> px -> rfg -> A
Ultimately, three parts are accepted. Adding up the x, m, a, and s rating for each of the accepted parts gives 7540 for the part with x=787, 4623 for the part with x=2036, and 6951 for the part with x=2127. Adding all of the ratings for all of the accepted parts gives the sum total of 19114.

Sort through all of the parts you've been given; what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?
--- Part Two ---
Even with your help, the sorting process still isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (x, m, a, s) can have an integer value ranging from a minimum of 1 to a maximum of 4000. Of all possible distinct combinations of ratings, your job is to figure out which ones will be accepted.

In the above example, there are 167409079868000 distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant. How many distinct combinations of ratings will be accepted by the Elves' workflows?
"""
import sys
from functools import reduce
from operator import mul


# Idea: https://www.reddit.com/r/adventofcode/comments/18ltr8m/comment/ke010be/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def solve():
    flows = {}
    for i, line in enumerate(input):
        if line == "\n":
            start = i
            break
        name, rules = line.strip().split("{")
        flows[name] = rules[:-1]

    # print(flows)
    def go_with(rule):
        # print(rule, ranges)
        if rule == "A":
            return reduce(mul, map(lambda x: x[1] - x[0] + 1, ranges.values()))
        elif rule == "R" or rule == "":
            return 0
        if rule in flows:
            rule = flows[rule]

        first = rule.split(",")[0]
        rest = rule[rule.find(",") + 1 :]
        alt_cond_range = None
        if ":" not in first:
            return go_with(first)
        cond, next = first.split(":")
        key = cond[0]
        old_range = ranges[key]
        x = int(cond[2:])
        if cond[1] == ">":
            cond_range = (x + 1, 4000)
            alt_cond_range = (1, x)
        else:
            cond_range = (1, x - 1)
            alt_cond_range = (x, 4000)
        new_range = intersect(old_range, cond_range)
        if new_range == (0, 0):
            return 0
        ranges[key] = new_range
        res = go_with(next)
        ranges[key] = old_range
        if alt_cond_range is not None:
            new_range = intersect(old_range, alt_cond_range)
            if new_range == (0, 0):
                return res
            ranges[key] = new_range
            res += go_with(rest)
            ranges[key] = old_range
        # print(rule, res)
        return res

    ranges = {
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    }
    res = go_with(flows["in"])
    print(res)


def intersect(a, b):
    x1, y1 = a
    x2, y2 = b
    return (
        (max(x1, x2), min(y1, y2))
        if (max(x1, x2) <= min(y1, y2) and max(x1, x2) > 0)
        else (0, 0)
    )


# def intersect(a, b):
#     intersection = []
#     for range1 in a:
#         for range2 in b:
#             start = max(range1[0], range2[0])
#             end = min(range1[1], range2[1])

#             if start <= end:
#                 intersection.append((start, end))
#     return intersection


# def union(a, b):
#     combined = sorted(a + b)
#     if not combined:
#         return []
#     # Initialize the result list with the first range
#     union = [combined[0]]

#     for current in combined[1:]:
#         last = union[-1]

#         if current[0] <= last[1] + 1:
#             new_range = (last[0], max(last[1], current[1]))
#             union[-1] = new_range
#         else:
#             union.append(current)
#     return union


# def invert(a):
#     sorted_ranges = sorted(a)

#     inverted = []
#     start = 0

#     for range in sorted_ranges:
#         # Add range from the end of the last range to the start of the current range
#         if start < range[0]:
#             inverted.append((start, range[0] - 1))
#         start = range[1] + 1

#     # Handle the end of the last range
#     if start <= 4000:
#         inverted.append((start, 4000))

#     return inverted


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve()
