import re       
from src.common.util import read_input
from itertools import chain

def parse_input(input):
    rules, messages = {}, []

    for line in input:
        rule_match = re.match(r'\d+:', line)

        if rule_match:
            rule_nr, rule_content = line.split(':')

            rule_nr = int(rule_nr)

            char_match = re.match(r'"([a-z])"', rule_content.strip())

            if char_match:
                rules[rule_nr] = char_match.group(1)
            else:
                rules[rule_nr] = [[int(i) for i in s.strip().split(' ')] for s in rule_content.split('|')]
        else:
            if line:
                messages.append(line)

    return rules, messages

def verify(messages, rules):
    def verify_helper(messages, current, rule_stack):
        while rule_stack:
            rule = rule_stack.pop()
            if isinstance(rule, str):
                return rule
            else:
                pass

    return verify_helper(sorted(messages, key=len), '', list(chain(*rules[0])))

def part_one(input):
    rules, messages = parse_input(input)

    return verify(messages, rules)

def part_two(input):
    return 0


def main():
    print('Day 19: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/input_day19.txt', '\n'))))
    print('Day 19: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/input_day19.txt', '\n'))))


if __name__ == "__main__":
    main()
