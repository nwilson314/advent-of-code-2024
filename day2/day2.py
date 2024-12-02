if __name__ == "__main__":
    with open("input.txt", "r") as f:
        reports = f.read().splitlines()

    def is_safe_levels(levels):
        inc = [levels[i+1] - levels[i] for i in range(len(levels)-1)]
        set_inc = set(inc)
        if set_inc <= {1,2,3} or set_inc <= {-1, -2, -3}:
            return True
        return False

    safe = 0
    safe_failed = 0
    for report in reports:
        levels = [int(x) for x in report.split()]
        if is_safe_levels(levels):
            safe += 1
        else:
            for i in range(len(levels)):
                if is_safe_levels(levels[:i]+levels[i+1:]):
                    safe_failed += 1
                    break

    print(f"part1: {safe}")
    print(f"part2: {safe_failed + safe}")