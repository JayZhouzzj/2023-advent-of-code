"""
The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
"""
import sys

digit_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def solve_line(line):
    def get_digit(i):
        if line[i].isdigit():
            return int(line[i])
        for key in digit_map:
            sub = line[i : i + len(key)]
            if sub == key:
                return digit_map[key]
        return None
    res = 0
    for i in range(len(line)):
        digit = get_digit(i)
        if digit:
            res += digit * 10
            break
    for i in range(len(line) - 1, -1, -1):
        digit = get_digit(i)
        if digit:
            res += digit
            break
    return res

def solve(input):
    sum = 0
    for line in input:
        line = line.strip()
        sum += solve_line(line)
    print(sum)


if __name__ == "__main__":
    # take input file name from cmd, default to input.txt
    if len(sys.argv) > 1:
        input = open(sys.argv[1], "r").readlines()
    else:
        input = open("input.txt", "r").readlines()
    solve(input)
