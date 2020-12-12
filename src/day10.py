from src.common.util import read_input


def get_differences(adapters):
    differences = {}

    for i in range(len(adapters) - 1):
        d = abs(adapters[i] - adapters[i + 1])
        differences[d] = differences[d] + 1 if d in differences else 1

    return differences


def part_one(input):
    adapters = [int(i) for i in input if i]

    adapter_chain = sorted(adapters)
    adapter_chain = [0] + adapter_chain + [adapter_chain[-1] + 3]

    diffs = get_differences(adapter_chain)

    return diffs[1] * diffs[3]


# def count_arrangements(current, remaining_adapters: list):
#     possibilites = []
#     next = remaining_adapters.pop(0)
#     while next :


def part_two(input):
    adapters = [int(i) for i in input if i]

    adapter_chain = sorted(adapters)

    #test = count_arrangements(0, adapter_chain)

    # for i in range(1, len(adapter_chain) - 1):
    #     d = abs(min_chain[-1] - adapter_chain[i + 1])
    #     if d > 3:
    #         min_chain.append(adapter_chain[i])
    #     else:
    #         remaining.append(adapter_chain[i])

    # min_chain.append(adapter_chain[-1])

    # chain_diff = len(adapter_chain) - len(min_chain)

    # print(min_chain, remaining)

    return 0


def main():
    print('Day 10: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/input_day10.txt', '\n'))))
    print('Day 10: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/input_day10.txt', '\n'))))


if __name__ == "__main__":
    main()
