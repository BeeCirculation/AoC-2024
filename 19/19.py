from functools import cache


def parse(fp):
    with open(fp, "r") as file:
        towels, patterns = file.read().split("\n\n")

    towels = towels.split(", ")
    patterns = patterns.split("\n")
    return set(towels), patterns[:-1]


towels, patterns = parse("input")


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
    out = []
    for i, pattern in enumerate(patterns):
        print(f"{i}/{len(patterns)}")
        out.append(find_all_towels(pattern))
    return out


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


arrangements = get_arrangements(patterns)
total = 0
for arrangement in arrangements:
    total += len(arrangement)
    print(arrangement)
print(total)
