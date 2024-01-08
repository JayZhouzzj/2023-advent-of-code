"""
You only have time to disconnect three wires.

Fortunately, someone left a wiring diagram (your puzzle input) that shows how the components are connected. For example:

jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
Each line shows the name of a component, a colon, and then a list of other components to which that component is connected. Connections aren't directional; abc: xyz and xyz: abc both represent the same configuration. Each connection between two components is represented only once, so some components might only ever appear on the left or right side of a colon.

In this example, if you disconnect the wire between hfx/pzl, the wire between bvb/cmg, and the wire between nvd/jqt, you will divide the components into two separate, disconnected groups:

9 components: cmg, frs, lhk, lsr, nvd, pzl, qnr, rsh, and rzs.
6 components: bvb, hfx, jqt, ntq, rhn, and xhk.
Multiplying the sizes of these groups together produces 54.

Find the three wires you need to disconnect in order to divide the components into two separate groups. What do you get if you multiply the sizes of these two groups together?
"""
import sys
from collections import defaultdict
import networkx as nx
import random


# Min cut with networkx idea: https://www.reddit.com/r/adventofcode/comments/18qbsxs/comment/ketzt6h/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
def solve_question():
    G = nx.Graph()
    for line in input:
        line = line.strip().split(" ")
        for node in line[1:]:
            G.add_edge(line[0][:-1], node, capacity=1)
    # print(sorted(list(G.nodes())))
    while True:
        try:
            start = random.choice(list(G.nodes()))
            end = random.choice(list(G.nodes()))
            cut_value, partition = nx.minimum_cut(G, start, end)
            if cut_value == 3:
                # print("Cut Value:", cut_value)
                partition = [sorted(list(x)) for x in partition]
                # print("One possible partition:", partition)
                print("Answer:", len(partition[0]) * len(partition[1]))
                break
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve_question()
