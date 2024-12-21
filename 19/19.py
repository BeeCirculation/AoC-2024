def parse(fp):
    with open(fp, "r") as file:
        towels, patterns = file.read().split("\n\n")

    towels = towels.split(", ")
    patterns = patterns.split("\n")
    return towels, patterns[:-1]


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


def get_all_towels(towels: list[str], patterns: list[str]) -> list[str]:
    out = []
    for pattern in patterns:
        out.append(find_towels(towels, pattern))
    return out


towels, patterns = parse("input")
print(len([a for a in get_all_towels(towels, patterns) if a]))
