with open("input.txt", "r") as f:
    lines = f.read().splitlines()


def grab_do(line, i, do):
    if line[i:i+7] == "don't()":
        return (False, i + 7)
    elif line[i:i+4] == "do()":
        return (True, i + 4)
    else:
        return (0, i + 1)

def grab_mul(line, i):
    munch = ""
    if line[i:i+4] == "mul(":
        i = i + 4
        start = i
        while line[i] != ")":
            if i - start > 7:
                return (0, start + 1)
            munch += line[i]
            i += 1
        nums = munch.split(",")
        if len(nums) != 2:
            return (0, start + 1)
        if not nums[0].isdigit() or not nums[1].isdigit():
            return (0, start + 1)
        return (int(nums[0]) * int(nums[1]), i + 1)
    else:
        return (0, i + 1)

total = 0
do_total = 0
do = True
for line in lines:
    i = 0
    while i < len(line):
        if line[i] == "d":
            (do, i) = grab_do(line, i, do)
        if line[i] == "m":
            (new_val, i) =  grab_mul(line, i)
            if do:
                do_total += new_val
            total += new_val
        else:
            i += 1

print(f"part1: {total}")
print(f"part2: {do_total}")