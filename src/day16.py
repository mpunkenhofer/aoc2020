import re
import operator
from functools import reduce
from src.common.util import read_input

def parse_input(input):
    rules = []
    my_ticket = []
    nearby_tickets = []

    it = iter(input)

    while (current := next(it, None)) is not None:
        if current.startswith('your ticket'):
            current = next(it, '')
            my_ticket = [int(i) for i in current.split(',')]
        elif current.startswith('nearby tickets'):
            while (current := next(it, None)) is not None:
                ticket = [int(i) for i in current.split(',')]
                nearby_tickets.append(ticket)
        else:
            rule_range_matches = re.findall(r'(\d+-\d+)', current)
            rule_name_match = re.match(r'([^:]+):', current)

            if rule_range_matches and rule_name_match:
                rules.append((rule_name_match.group(1), list(map(lambda x: [int(i) for i in x.split('-')], rule_range_matches))))

    return rules, my_ticket, nearby_tickets

def verify_ticket_any_rule(ticket, rules):
    invalid_fields = []

    ranges = sum([range for _, range in rules], [])

    for field in ticket:
        if not any(map(lambda r: r[0] <= field <= r[1], ranges)):
            invalid_fields.append(field)

    return invalid_fields

def valid_fields(tickets, rules):
    rules_dict = {rule: i + 1 for i, rule in enumerate(rules)}

    g = Glucose3()

    for ticket in tickets:
        for field in ticket:
            clause = []

            for rule, ranges in rules:
                for r in ranges:
                    if r[0] <= field <= r[1]:
                        clause.append(rules_dict[rule])
                    else:
                        clause.append(-rules_dict[rule])

            g.add_clause(clause)

    return []
    
def part_one(input):
    rules, _, nearby_tickets = parse_input(input)

    return sum(reduce(lambda x, y: x+y, map(lambda ticket: verify_ticket_any_rule(ticket, rules), nearby_tickets)))


def part_two(input, interesting_fields='departure'):
    rules, my_ticket, nearby_tickets = parse_input(input) #parse_input(read_input('tests/inputs/test_input_day16_2.txt', '\n'))
    valid_tickets = filter(lambda ticket: len(verify_ticket_any_rule(ticket, rules)) == 0, nearby_tickets)
    
    ticket_rules = []

    for ticket in valid_tickets:
        field_rules = []

        for field in ticket:
            possible_rules = []

            for rule, ranges in rules:
                for r in ranges:
                    if r[0] <= field <= r[1]:
                        possible_rules.append(rule)
                        break

            field_rules.append((field, possible_rules))

        ticket_rules.append(field_rules)

    reduced_ticket_rules = []
    for i in range(len(ticket_rules[0])):
        reduced_ticket_rules.append(list(reduce(lambda x, y: set(x) & set(y), map(lambda tr: tr[i][1], ticket_rules))))

    order = [] 

    while reduced_ticket_rules:
        reduced_ticket_rules = sorted(reduced_ticket_rules, key=len)
        rule = reduced_ticket_rules[0][0]
        reduced_ticket_rules = reduced_ticket_rules[1:]
        reduced_ticket_rules = list(map(lambda x: list(set(x) - set([rule])), reduced_ticket_rules))
        order.append(rule)

    relevant_fields = filter(lambda x: interesting_fields in x[1], enumerate(order))
    return reduce((lambda x, y: x * y), map(lambda f: my_ticket[f[0]], relevant_fields))

def main():
    print('Day 16: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/input_day16.txt', '\n'))))
    print('Day 16: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/input_day16.txt', '\n'))))


if __name__ == "__main__":
    main()
