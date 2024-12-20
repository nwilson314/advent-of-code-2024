'''
--- Day 16: Reindeer Maze ---
It's time again for the Reindeer Olympics! This year, the big event is the Reindeer Maze, where the Reindeer compete for the lowest score.

You and The Historians arrive to search for the Chief right as the event is about to start. It wouldn't hurt to watch a little, right?

The Reindeer start on the Start Tile (marked S) facing East and need to reach the End Tile (marked E). They can move forward one tile at a time (increasing their score by 1 point), but never into a wall (#). They can also rotate clockwise or counterclockwise 90 degrees at a time (increasing their score by 1000 points).

To figure out the best place to sit, you start by grabbing a map (your puzzle input) from a nearby kiosk. For example:

###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
There are many paths through this maze, but taking any of the best paths would incur a score of only 7036. This can be achieved by taking a total of 36 steps forward and turning 90 degrees a total of 7 times:


###############
#.......#....E#
#.#.###.#.###^#
#.....#.#...#^#
#.###.#####.#^#
#.#.#.......#^#
#.#.#####.###^#
#..>>>>>>>>v#^#
###^#.#####v#^#
#>>^#.....#v#^#
#^#.#.###.#v#^#
#^....#...#v#^#
#^###.#.#.#v#^#
#S..#.....#>>^#
###############
Here's a second example:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
In this maze, the best paths cost 11048 points; following one such path would look like this:

#################
#...#...#...#..E#
#.#.#.#.#.#.#.#^#
#.#.#.#...#...#^#
#.#.#.#.###.#.#^#
#>>v#.#.#.....#^#
#^#v#.#.#.#####^#
#^#v..#.#.#>>>>^#
#^#v#####.#^###.#
#^#v#..>>>>^#...#
#^#v###^#####.###
#^#v#>>^#.....#.#
#^#v#^#####.###.#
#^#v#^........#.#
#^#v#^#########.#
#S#>>^..........#
#################
Note that the path shown above includes one 90 degree turn as the very first move, rotating the Reindeer from facing East to facing North.

Analyze your map carefully. What is the lowest score a Reindeer could possibly get?

Your puzzle answer was 85432.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Now that you know what the best paths look like, you can figure out the best spot to sit.

Every non-wall tile (S, ., or E) is equipped with places to sit along the edges of the tile. While determining which of these tiles would be the best spot to sit depends on a whole bunch of factors (how comfortable the seats are, how far away the bathrooms are, whether there's a pillar blocking your view, etc.), the most important factor is whether the tile is on one of the best paths through the maze. If you sit somewhere else, you'd miss all the action!

So, you'll need to determine which tiles are part of any best path through the maze, including the S and E tiles.

In the first example, there are 45 tiles (marked O) that are part of at least one of the various best paths through the maze:

###############
#.......#....O#
#.#.###.#.###O#
#.....#.#...#O#
#.###.#####.#O#
#.#.#.......#O#
#.#.#####.###O#
#..OOOOOOOOO#O#
###O#O#####O#O#
#OOO#O....#O#O#
#O#O#O###.#O#O#
#OOOOO#...#O#O#
#O###.#.#.#O#O#
#O..#.....#OOO#
###############
In the second example, there are 64 tiles that are part of at least one of the best paths:

#################
#...#...#...#..O#
#.#.#.#.#.#.#.#O#
#.#.#.#...#...#O#
#.#.#.#.###.#.#O#
#OOO#.#.#.....#O#
#O#O#.#.#.#####O#
#O#O..#.#.#OOOOO#
#O#O#####.#O###O#
#O#O#..OOOOO#OOO#
#O#O###O#####O###
#O#O#OOO#..OOO#.#
#O#O#O#####O###.#
#O#O#OOOOOOO..#.#
#O#O#O#########.#
#O#OOO..........#
#################
Analyze your map further. How many tiles are part of at least one of the best paths through the maze?
'''
from collections import deque
from enum import Enum

def parse_input(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()

        return lines

class Direction(str, Enum):
    E = 'E'
    N = 'N'
    W = 'W'
    S = 'S'

    def get_move(self):
        dirs = {
            'E': (0, 1),
            'N': (-1, 0),
            'W': (0, -1),
            'S': (1, 0)
        }
        return dirs[self.value]

    @classmethod
    def rotate_left(cls, cur_dir):
        dirs = {
            cls.E: cls.N,
            cls.N: cls.W,
            cls.W: cls.S,
            cls.S: cls.E
        }
        return dirs[cur_dir]

    @classmethod
    def rotate_right(cls, cur_dir):
        dirs = {
            cls.E: cls.S,
            cls.N: cls.E,
            cls.W: cls.N,
            cls.S: cls.W
        }
        return dirs[cur_dir]


def bfs(grid, start_pos, end_pos, cur_pos, cur_dir, visited, score):
    pass

def solve_part1(grid, start_pos, end_pos):
    q = deque()
    cur_dir = Direction.E
    visited = dict()
    score = 0
    path = set(start_pos)
    optimal_path = set()

    state = (start_pos, cur_dir)
    visited[state] = score
    q.append((start_pos, cur_dir, score, path))

    min_score = float('inf')

    while q:
        cur_pos, cur_dir, score, path = q.popleft()
        # print(f"cur_pos: {cur_pos}, cur_dir: {cur_dir}, score: {score}")
        if cur_pos == end_pos:
            if score == min_score:
                optimal_path = optimal_path.union(path)
            elif score < min_score:
                min_score = score
                optimal_path = path
            continue
        
        ##  Gather moves
        # Forward
        forward = (cur_pos[0] + cur_dir.get_move()[0], cur_pos[1] + cur_dir.get_move()[1])
        if grid[forward[0]][forward[1]] != '#' and (forward, cur_dir) not in visited:
            q.append((forward, cur_dir, score + 1, path.union({forward})))
            visited[(forward, cur_dir)] = score + 1
        elif (forward, cur_dir) in visited and score + 1 < visited[(forward, cur_dir)]:
            visited[(forward, cur_dir)] = score + 1
            q.append((forward, cur_dir, score + 1, path.union({forward})))
        elif (forward, cur_dir) in visited and score + 1 == visited[(forward, cur_dir)]:
            q.append((forward, cur_dir, score + 1, path.union({forward})))
        
        # Rotate left
        left_dir = Direction.rotate_left(cur_dir)
        if (cur_pos, left_dir) not in visited:
            q.append((cur_pos, left_dir, score + 1000, path))
            visited[(cur_pos, left_dir)] = score + 1000
        elif (cur_pos, left_dir) in visited and score + 1000 < visited[(cur_pos, left_dir)]:
            visited[(cur_pos, left_dir)] = score + 1000
            q.append((cur_pos, left_dir, score + 1000, path))
        elif (cur_pos, left_dir) in visited and score + 1000 == visited[(cur_pos, left_dir)]:
            q.append((cur_pos, left_dir, score + 1000, path))
        
        # Rotate right
        right_dir = Direction.rotate_right(cur_dir)
        if (cur_pos, right_dir) not in visited:
            q.append((cur_pos, right_dir, score + 1000, path))
            visited[(cur_pos, right_dir)] = score + 1000
        elif (cur_pos, right_dir) in visited and score + 1000 < visited[(cur_pos, right_dir)]:
            visited[(cur_pos, right_dir)] = score + 1000
            q.append((cur_pos, right_dir, score + 1000, path))
        elif (cur_pos, right_dir) in visited and score + 1000 == visited[(cur_pos, right_dir)]:
            q.append((cur_pos, right_dir, score + 1000, path))
    return min_score, optimal_path


if __name__ == "__main__":
    lines = parse_input("input.txt")

    grid = [list(line) for line in lines]

    for i, row in enumerate(grid):
        if 'S' in row:
            start_pos = (i, row.index('S'))
        if 'E' in row:
            end_pos = (i, row.index('E'))

    score, optimal_path = solve_part1(grid, start_pos, end_pos)
    count = 0
    for path in optimal_path:
        print(path)
        # if path != start_pos and path != end_pos:
        count += 1
    

    print(f"Part 1: {score}")
    print(f"Part 2: {count}")