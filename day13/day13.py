'''
--- Day 13: Claw Contraption ---
Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.
The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

Your puzzle answer was 36838.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
As you go to win the first prize, you discover that the claw is nowhere near where you expected it would be. Due to a unit conversion error in your measurements, the position of every prize is actually 10000000000000 higher on both the X and Y axis!

Add 10000000000000 to the X and Y position of every prize. After making this change, the example above would now look like this:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=10000000008400, Y=10000000005400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=10000000012748, Y=10000000012176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=10000000007870, Y=10000000006450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=10000000018641, Y=10000000010279
Now, it is only possible to win a prize on the second and fourth claw machines. Unfortunately, it will take many more than 100 presses to do so.

Using the corrected prize coordinates, figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?
'''

with open("input.txt", "r") as f:
    rows = f.read().splitlines()

move_set = []
machines = []
for row in rows:
    if row == "":
        machines.append(move_set)
        move_set = []
        continue
    if len(move_set) < 2:
        # A and B button
        button = row.split(": ")[0].split(" ")[1]
        x = row.split(": ")[1].strip().split(", ")[0].split("+")[1]
        y = row.split(": ")[1].strip().split(", ")[1].split("+")[1]
        move_set.append((button, int(x), int(y)))
    else:
        # Prize
        x = row.split(": ")[1].strip().split(", ")[0].split("=")[1]
        y = row.split(": ")[1].strip().split(", ")[1].split("=")[1]
        move_set.append(("Prize",int(x), int(y)))

if move_set:  # Add the last move_set if it exists
    machines.append(move_set)

a_price = 3
b_price = 1

def calc_price(move_set, memo=None):
    if memo is None:
        memo = {}
        
    def dp(a_moves, b_moves):
        if (a_moves, b_moves) in memo:
            return memo[(a_moves, b_moves)]
            
        if a_moves > 100 or b_moves > 100:
            return float('inf')
            
        a_button = (move_set[0][1], move_set[0][2])
        b_button = (move_set[1][1], move_set[1][2])
        prize = (move_set[2][1], move_set[2][2])
        
        # Calculate current position
        cur_x = a_moves * a_button[0] + b_moves * b_button[0]
        cur_y = a_moves * a_button[1] + b_moves * b_button[1]
        
        # If we've gone too far
        if cur_x > prize[0] or cur_y > prize[1]:
            return float('inf')
            
        # If we've reached the prize
        if cur_x == prize[0] and cur_y == prize[1]:
            return a_moves * a_price + b_moves * b_price
            
        # Try both buttons
        try_a = dp(a_moves + 1, b_moves)
        try_b = dp(a_moves, b_moves + 1)
        
        result = min(try_a, try_b)
        memo[(a_moves, b_moves)] = result
        return result
        
    return dp(0, 0)

total_cost = 0
for machine in machines:
    price = calc_price(machine)
    if price < float('inf'):
        # print(f"machine: {machine}, price: {price}")
        total_cost += price
    
print(f"part1: {total_cost}")

def calc_price2(move_set):
    a_button = (move_set[0][1], move_set[0][2])
    b_button = (move_set[1][1], move_set[1][2])
    prize = (move_set[2][1], move_set[2][2])
    
    target_x = prize[0] + 10000000000000
    target_y = prize[1] + 10000000000000
    
    # Need to solve:
    # a_moves * a_x + b_moves * b_x = target_x
    # a_moves * a_y + b_moves * b_y = target_y
    
    # Using Cramer's rule to solve the system of equations
    determinant = a_button[0] * b_button[1] - a_button[1] * b_button[0]
    
    if determinant == 0:
        # No solution exists
        return float('inf')  
        
    a_moves = (target_x * b_button[1] - b_button[0] * target_y) / determinant
    b_moves = (a_button[0] * target_y - target_x * a_button[1]) / determinant
    
    if not (a_moves.is_integer() and b_moves.is_integer()):
        return float('inf')
        
    a_moves = int(a_moves)
    b_moves = int(b_moves)
    
    if a_moves < 0 or b_moves < 0:
        return float('inf')
        
    return a_moves * a_price + b_moves * b_price

total_cost = 0
for machine in machines:
    price = calc_price2(machine)
    if price < float('inf'):
        print(f"machine: {machine}, price: {price}")
        total_cost += price
    
print(f"part2: {total_cost}")