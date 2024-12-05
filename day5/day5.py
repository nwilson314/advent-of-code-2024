with open("input.txt", "r") as f:
    lines = f.read().splitlines()


for i, line in enumerate(lines):
    if line == "":
        orders = lines[:i]
        updates = lines[i+1:]
        break


from collections import defaultdict
order_mp = defaultdict(list)
for order in orders:
    before, after = order.split("|")
    order_mp[before].append(after)

def fix_bad_update(items):
    order = [len(items)] * len(items)

    for i, item in enumerate(items):
        ordered = order_mp[item]
        for item2 in ordered:
            if item2 in items:
                order[i] -= 1

    new_items = zip(items, order)
    new_items = sorted(new_items, key=lambda x: x[1])
    new_items = [x[0] for x in new_items]

    return int(new_items[len(new_items)//2])

total = 0
bad_total = 0
for update in updates:
    items = update.split(",")
    bad_update = False
    for i, item in enumerate(items):
        set_i = set(order_mp[item])
        if set(items[:i]).intersection(set_i):
            bad_update = True
            bad_total += fix_bad_update(items)
            break
    if not bad_update:
        total += int(items[len(items)//2])

print(f"part1: {total}")
print(f"part2: {bad_total}")