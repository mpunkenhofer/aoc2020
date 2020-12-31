import re
from src.common.util import read_input


def parse_input(input):
    result = {}

    for line in input:
        foods, allergens = line.split('(')
        allergens_match = re.match(r'contains (.+)\)', allergens)

        if allergens_match:
            allergens = allergens_match.group(1).split(', ')
            foods = foods.strip().split(' ')

            for allergen in allergens:
                if allergen in result:
                    result[allergen] |= set(foods)
                else:
                    result[allergen] = set(foods)

    return result

def part_one(input):
    allergene_list = parse_input(input)

    test = set.difference(*allergene_list.values())

    return 0


def part_two(input):
    return 0


def main():
    print('Day 21: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/input_day21.txt', '\n'))))
    print('Day 21: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/input_day21.txt', '\n'))))


if __name__ == "__main__":
    main()
