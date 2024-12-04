"""
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....
The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
Take a look at the little Elf's word search. How many times does XMAS appear?
"""

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

def find_xmas(lines, i, j, i_inc, j_inc, cur_char):
    if cur_char == "S":
        return True
    if i +i_inc < 0 or i + i_inc >= len(lines):
        return False
    if j + j_inc < 0 or j + j_inc >= len(lines[i]):
        return False
    match cur_char:
        case "X":
            if lines[i+i_inc][j+j_inc] == "M":
                return find_xmas(lines, i+i_inc, j+j_inc, i_inc, j_inc, "M")
            else:
                return False
        case "M":
            if lines[i+i_inc][j+j_inc] == "A":
                return find_xmas(lines, i+i_inc, j+j_inc, i_inc, j_inc, "A")
            else:
                return False
        case "A":
            if lines[i+i_inc][j+j_inc] == "S":
                return find_xmas(lines, i+i_inc, j+j_inc, i_inc, j_inc, "S")
            else:
                return False
        case _:
            return False


total = 0
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "X":
            forward = find_xmas(lines, i, j, 0, 1, "X")
            backward = find_xmas(lines, i, j, 0, -1, "X")
            up = find_xmas(lines, i, j, -1, 0, "X")
            down = find_xmas(lines, i, j, 1, 0, "X")
            diag_up_l = find_xmas(lines, i, j, -1, -1, "X")
            diag_up_r = find_xmas(lines, i, j, -1, 1, "X")
            diag_down_l = find_xmas(lines, i, j, 1, -1, "X")
            diag_down_r = find_xmas(lines, i, j, 1, 1, "X")
            total += int(forward) + int(backward) + int(up) + int(down) + int(diag_up_l) + int(diag_up_r) + int(diag_down_l) + int(diag_down_r)

print(f"part1: {total}")

"""
--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S
Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........
In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?

"""

def find_cross_mas(lines, i, j):
    if i + 1 >= len(lines) or i - 1 < 0:
        return False
    if j + 1 >= len(lines[i]) or j - 1 < 0:
        return False

    if lines[i-1][j-1] == "M":
        if lines[i-1][j+1] == "M":
            return lines[i+1][j-1] == "S" and lines[i+1][j+1] == "S"
        elif lines[i+1][j-1] == "M":
            return lines[i+1][j+1] == "S" and lines[i-1][j+1] == "S"
        else:
            return False
    elif lines[i+1][j+1] == "M":
        if lines[i-1][j+1] == "M":
            return lines[i-1][j-1] == "S" and lines[i+1][j-1] == "S"
        elif lines[i+1][j-1] == "M":
            return lines[i-1][j-1] == "S" and lines[i-1][j+1] == "S"
        else:
            return False
    else:
        return False
        

total = 0

for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "A":
            if find_cross_mas(lines, i, j):
                total += 1

print(f"part2: {total}")