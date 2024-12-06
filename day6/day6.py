"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
"""

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


for i, row in enumerate(lines):
    for j, col in enumerate(row):
        if col == "^":
            start_i, start_j = i, j
            break

grid = [list(row) for row in lines]

unique_pos = set()

start_pos = (start_i, start_j)
pos = start_pos
start_dr = (-1, 0)
dr = start_dr
dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def traverse(pos, dr):
    while grid[pos[0]][pos[1]] != "#":
        unique_pos.add(pos)
        pos = (pos[0] + dr[0], pos[1] + dr[1])
        if pos[0] >= len(grid) or pos[0] < 0 or pos[1] >= len(grid[0]) or pos[1] < 0:
            return pos
        
    pos = (pos[0] - dr[0], pos[1] - dr[1])
    return pos

while True:
    pos = traverse(pos, dr)
    if pos[0] >= len(grid) or pos[0] < 0 or pos[1] >= len(grid[0]) or pos[1] < 0:
        exit_pos = pos
        break 
    else:
        dr = dirs[(dirs.index(dr) + 1) % 4]

print(f"exit pos: {exit_pos}")
count = len(unique_pos)

print(f"part1: {count}")

"""
--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
"""


def simulate_with_obstacle(start_pos, start_dr, obstacle_pos, debug=False):
    pos = start_pos
    dr = start_dr
    visited_states = set()  # Track (position, direction) pairs
    
    if debug:
        debug_grid = [list(row) for row in grid]
        debug_grid[obstacle_pos[0]][obstacle_pos[1]] = 'O'
    
    while True:
        state = (pos, dr)
        if state in visited_states:
            if debug:
                print(f"\nLoop found with obstacle at {obstacle_pos}")
                print("Path visualization:")
                for row in debug_grid:
                    print(''.join(row))
            return True
        
        visited_states.add(state)
        
        if debug and pos != start_pos:
            if dr in [(-1, 0), (1, 0)]:  # vertical movement
                debug_grid[pos[0]][pos[1]] = '|'
            else:  # horizontal movement
                debug_grid[pos[0]][pos[1]] = '-'
        
        next_pos = (pos[0] + dr[0], pos[1] + dr[1])
        
        # Check if we hit a wall, obstacle, or boundary
        if ((next_pos[0] < len(grid) and next_pos[0] >= 0 and 
            next_pos[1] < len(grid[0]) and next_pos[1] >= 0) and
            (grid[next_pos[0]][next_pos[1]] == "#" or 
            next_pos == obstacle_pos)):
            dr = dirs[(dirs.index(dr) + 1) % 4]  # Turn right
        else:
            pos = next_pos
            if (pos[0] >= len(grid) or pos[0] < 0 or 
                pos[1] >= len(grid[0]) or pos[1] < 0):
                return False
        
        # Prevent infinite paths
        if len(visited_states) > len(grid) * len(grid[0]) * 4:
            return False
    
    return False

# Find valid obstacle positions
valid_positions = []

# Try each empty position
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == "#" or (i, j) == start_pos:
            continue
            
        if simulate_with_obstacle(start_pos, start_dr, (i, j)):
            valid_positions.append((i, j))

print(f"part2: {len(valid_positions)}")

# Debug: Show first few solutions
print("\nFirst 3 solutions:")
for pos in valid_positions[:3]:
    simulate_with_obstacle(start_pos, start_dr, pos, debug=True)
