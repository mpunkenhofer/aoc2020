from src.common.util import read_input

def input_to_list(input):
    password_infos = []

    for line in input:
        r, l, p = line.split(' ')
        r = r.split('-')
        password_infos.append(((int(r[0]), int(r[1])), l[0], p))
    
    return password_infos

        

def is_valid_part_one(password_info):
    (r_start, r_end), letter, password = password_info
    letter_count = password.count(letter)
    return r_start <= letter_count <= r_end

def is_valid_part_two(password_info):
    (p1, p2), letter, password = password_info
    p1, p2 = p1 - 1, p2 - 1
    password_len = len(password)
    occurences = 0

    if p1 < password_len and password[p1] == letter:
        occurences = occurences + 1
    
    if p2 < password_len and password[p2] == letter:
        occurences = occurences + 1
    
    return occurences == 1

def part_one(input):
    password_infos = input_to_list(input)
    return sum(map(is_valid_part_one, password_infos))


def part_two(input):
    password_infos = input_to_list(input)
    return sum(map(is_valid_part_two, password_infos))


def main():
    print('Day 2: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/input_day2.txt', '\n'))))
    print('Day 2: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/input_day2.txt', '\n'))))


if __name__ == "__main__":
    main()
