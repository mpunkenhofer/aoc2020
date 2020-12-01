from src.common.util import read_input


def part_one(input):
    expenses_report = [int(i) for i in input]

    for a in expenses_report:
        for b in expenses_report:
            if a + b == 2020:
                return a * b
    
    return 0


def part_two(input):
    expenses_report = [int(i) for i in input]

    for a in expenses_report:
        for b in expenses_report:
            for c in expenses_report:
                if a + b + c == 2020:
                    return a * b * c
    
    return 0


def main():
    print('Day 1: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/day1/input', '\n'))))
    print('Day 1: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/day1/input', '\n'))))


if __name__ == "__main__":
    main()
