"""
--- Day 8: Resonant Collinearity ---
You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........
Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.
Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?

Your puzzle answer was 400.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Watching over your shoulder as you work, one of The Historians asks if you took the effects of resonant harmonics into your calculations.

Whoops!

After updating your model, it turns out that an antinode occurs at any grid position exactly in line with at least two antennas of the same frequency, regardless of distance. This means that some of the new antinodes will occur at the position of each antenna (unless that antenna is the only one of its frequency).

So, these three T-frequency antennas now create many antinodes:

T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
In fact, the three T-frequency antennas are all exactly in line with two antennas, so they are all also antinodes! This brings the total number of antinodes in the above example to 9.

The original example now has 34 antinodes, including the antinodes that appear on every antenna:

##....#....#
.#.#....0...
..#.#0....#.
..##...0....
....0....#..
.#...#A....#
...#..#.....
#....#.#....
..#.....A...
....#....A..
.#........#.
...#......##
Calculate the impact of the signal using this updated model. How many unique locations within the bounds of the map contain an antinode?
"""

with open("input.txt", "r") as f:
    rows = f.read().splitlines()

grid = [list(row) for row in rows]

antenna_map = {}

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == ".":
            continue
        if grid[i][j] in antenna_map:
            antenna_map[grid[i][j]].append((i, j))
        else:
            antenna_map[grid[i][j]] = [(i, j)]


def find_antinodes(ant1, ant2):
    y1, x1 = ant1
    y2, x2 = ant2

    dy = y2 - y1
    dx = x2 - x1

    # print(f"ant1 ({grid[y1][x1]}): {ant1}, ant2 ({grid[y2][x2]}): {ant2}")
    # print(f"dy: {dy}, dx: {dx}")

    antinodes = []

    antinode1 = (y2 + dy, x2 + dx) # antinode for ant1 -> distance to ant2 and then going further
    antinode2 = (y1 - dy, x1 - dx)

    # print(f"antinode1: {antinode1}, antinode2: {antinode2}")

    if antinode1[0] >= 0 and antinode1[0] < len(grid) and antinode1[1] >= 0 and antinode1[1] < len(grid[0]):
        antinodes.append(antinode1)

    if antinode2[0] >= 0 and antinode2[0] < len(grid) and antinode2[1] >= 0 and antinode2[1] < len(grid[0]):
        antinodes.append(antinode2)

    return antinodes


def find_resonant_antinodes(ant1, ant2):
    y1, x1 = ant1
    y2, x2 = ant2

    dy = y2 - y1
    dx = x2 - x1

    antinodes = [ant1, ant2]

    while y2 + dy >= 0 and y2 + dy < len(grid) and x2 + dx >= 0 and x2 + dx < len(grid[0]):
        antinodes.append((y2 + dy, x2 + dx))
        y2 += dy
        x2 += dx

    while y1 - dy >= 0 and y1 - dy < len(grid) and x1 - dx >= 0 and x1 - dx < len(grid[0]):
        antinodes.append((y1 - dy, x1 - dx))
        y1 -= dy
        x1 -= dx

    return antinodes

unique_antinodes = set()
unique_resonant_antinodes = set()

for ant in antenna_map:
    for i, pos in enumerate(antenna_map[ant]):
        for j in range(i + 1, len(antenna_map[ant])):
            ant2 = antenna_map[ant][j]
            antinodes = find_antinodes(pos, ant2)
            unique_antinodes.update(antinodes)

            antinodes = find_resonant_antinodes(pos, ant2)
            unique_resonant_antinodes.update(antinodes)

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if (i, j) in unique_antinodes and grid[i][j] == ".":
            grid[i][j] = "#"

print("\n".join(["".join(row) for row in grid]))


print(f"part1: {len(unique_antinodes)}")
print(f"part2: {len(unique_resonant_antinodes)}")