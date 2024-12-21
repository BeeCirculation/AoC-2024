from functools import cache


def parse(fp):
    with open(fp, "r") as file:
        towels, patterns = file.read().split("\n\n")

    towels = towels.split(", ")
    patterns = patterns.split("\n")
    return set(towels), patterns[:-1]


towels, patterns = parse("input")
longest = max(map(len, towels))

def find_towels(towels: list[str], pattern: str) -> list[str] | None:
    for towel in towels:
        if towel == pattern:
            return [towel]

        if pattern.startswith(towel):
            more_towels = find_towels(towels, pattern[pattern.find(towel) + len(towel):])
            if not more_towels:
                continue
            return [towel] + more_towels
    return None


def get_arrangements(patterns: list[str]) -> list[str]:
    total =0
    for i, pattern in enumerate(patterns):
        print(f"{i}/{len(patterns)}")
        total += count_all_towels(pattern)
    return total


@cache
def find_all_towels(pattern: str) -> tuple[tuple[str]] | None:
    o = []
    for towel in towels:
        if towel == pattern:
            o.append(tuple(towel))
        elif pattern.startswith(towel):
            more_towels = find_all_towels(pattern[pattern.find(towel) + len(towel):])
            if not more_towels:
                continue
            for arrangement in more_towels:
                o.append(tuple([towel] + list(arrangement)))
    return tuple(o)


@cache
def count_all_towels(pattern: str) -> int:
    if pattern == "":
        return 1

    arrangements = 0
    for i in range(min(len(pattern), longest)):
        substr = pattern[:i+1]
        if substr in towels:
            arrangements += count_all_towels(pattern[i+1:])
    return arrangements


print(get_arrangements(patterns))
