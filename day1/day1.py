
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        locations = f.read().splitlines()

    loc_ids1 = []
    loc_ids2 = []
    right_mp = {}
    for location in locations:
        (left, right) = location.split()
        left = int(left)
        right = int(right)
        if right not in right_mp:
            right_mp[right] = 1
        else:
            right_mp[right] += 1
        if left not in right_mp:
            right_mp[left] = 0
        loc_ids1.append(left)
        loc_ids2.append(right)

    loc_ids1.sort()
    loc_ids2.sort()

    diff = 0
    sim = 0
    for i in range(len(loc_ids1)):
        diff += abs(loc_ids1[i] - loc_ids2[i])
        sim += loc_ids1[i] * right_mp[loc_ids1[i]]
    
    print(f"part1 diff: {diff}")
    print(f"part2 sim: {sim}")