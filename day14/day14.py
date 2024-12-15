'''
--- Day 14: Restroom Redoubt ---
One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...
These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........
The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....
To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....
           
..... .....
...12 .....
.1... 1....
In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?

Your puzzle answer was 219512160.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?

'''
with open("input.txt", "r") as f:
    rows = f.read().splitlines()

width, height = 101, 103
t = 100  # Part 1 uses exactly 100 seconds

def wrap(pos, min_val, max_val):
    return ((pos - min_val) % (max_val - min_val)) + min_val

# Initialize robots with their starting positions and velocities
robots = []
for row in rows:
    p, v = row.split(" ")
    x, y = map(int, p.split("=")[1].split(","))
    vx, vy = map(int, v.split("=")[1].split(","))
    robots.append((x, y, vx, vy))

# Create new grid after time t
new_grid = {}
for x, y, vx, vy in robots:
    # Calculate final position after t seconds
    final_x = wrap(x + vx * t, 0, width)
    final_y = wrap(y + vy * t, 0, height)
    
    if final_y not in new_grid:
        new_grid[final_y] = {}
    if final_x not in new_grid[final_y]:
        new_grid[final_y][final_x] = []
    new_grid[final_y][final_x].append((vx, vy))

# Find middle points (integer division)
mid_x = width // 2
mid_y = height // 2

# Count robots in each quadrant
q1 = 0  # top-right
q2 = 0  # top-left
q3 = 0  # bottom-left
q4 = 0  # bottom-right

for j in range(height):
    for i in range(width):
        if j not in new_grid or i not in new_grid[j] or not new_grid[j][i]:
            continue
            
        # Skip robots on the middle lines
        if i == mid_x or j == mid_y:
            continue
            
        num_robots = len(new_grid[j][i])
        
        if i < mid_x:
            if j < mid_y:
                q2 += num_robots  # top-left
            else:
                q3 += num_robots  # bottom-left
        else:
            if j < mid_y:
                q1 += num_robots  # top-right
            else:
                q4 += num_robots  # bottom-right

safety_factor = q1 * q2 * q3 * q4
print(f"Quadrant counts: {q1}, {q2}, {q3}, {q4}")
print(f"Safety factor: {safety_factor}")

def visualize_grid(grid):
    output = []
    for j in range(height):
        row = ""
        for i in range(width):
            if j in grid and i in grid[j] and grid[j][i]:
                row += '#'
            else:
                row += '.'
        output.append(row)
    print('\n'.join(output))

def count_connected_robots(grid):
    visited = set()
    
    def get_neighbors(y, x):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                ny, nx = y + dy, x + dx
                if (0 <= ny < height and 0 <= nx < width and 
                    ny in grid and nx in grid[ny] and grid[ny][nx]):
                    yield (ny, nx)
    
    # Find the largest connected component
    max_component_size = 0
    total_robots = 0
    
    for y in grid:
        for x in grid[y]:
            if not grid[y][x] or (y, x) in visited:
                continue
                
            # Count robots in this position
            total_robots += len(grid[y][x])
            
            if (y, x) in visited:
                continue
                
            # Start a new component
            component_size = len(grid[y][x])  # Count robots at start position
            stack = [(y, x)]
            visited.add((y, x))
            
            while stack:
                cy, cx = stack.pop()
                for ny, nx in get_neighbors(cy, cx):
                    if (ny, nx) not in visited:
                        visited.add((ny, nx))
                        component_size += len(grid[ny][nx])
                        stack.append((ny, nx))
            
            max_component_size = max(max_component_size, component_size)
    
    return max_component_size, total_robots

# Try different time steps
print("\nSearching for connected patterns...")
for t in range(0, 10000):  # Check every step up to 10000
    new_grid = {}
    for x, y, vx, vy in robots:
        final_x = wrap(x + vx * t, 0, width)
        final_y = wrap(y + vy * t, 0, height)
        
        if final_y not in new_grid:
            new_grid[final_y] = {}
        if final_x not in new_grid[final_y]:
            new_grid[final_y][final_x] = []
        new_grid[final_y][final_x].append((vx, vy))
    
    largest_component, total = count_connected_robots(new_grid)
    if largest_component >= total * 0.8:  # 80% of robots are connected
        print(f"\nFound highly connected pattern at time {t}!")
        print(f"Connected robots: {largest_component}/{total} ({largest_component/total*100:.1f}%)")
        visualize_grid(new_grid)
        print("-" * 50)
