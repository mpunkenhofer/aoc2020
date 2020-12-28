import re
import numpy as np
from src.common.util import read_input
from itertools import groupby, chain
from functools import reduce


def get_ascii_edge_image(edge, size):
    if size > 1:
        top, right, bot, left = edge
        spaces = size - 2

        top_line, bot_line = '', ''
        center = []

        for i in range(size):
            top_line += '#' if top & 1 << i else '.'
            bot_line += '#' if bot & 1 << i else '.'

            center.append(('#' if left & 1 << i else '.') + ' ' *
                          spaces + ('#' if right & 1 << i else '.'))

        frame = [top_line] + center[1:-1] + [bot_line]

        # for line in frame:
        #     print(line)

        return frame
    return []


def get_ascii_image(image, size):
    if size > 0:
        ascii_image = []

        for image_line in image:
            line = ''
            for i in range(size):
                line += '#' if image_line & 1 << i else '.'
            # print(line)
            ascii_image.append(line)

        return ascii_image

    return []


def tiles_fit(tile_a, tile_b):
    for orientation_a in tile_a:
        for edge_a in orientation_a:
            for orentation_b in tile_b:
                for edge_b in orentation_b:
                    if edge_a == edge_b:
                        return True

    return False


def get_fitting_tiles(edges):
    fitting_tiles = {}
    edge_list = list(edges.items())

    for i in range(len(edge_list)):
        for j in range(i + 1, len(edge_list)):
            (tile_a_id, tile_a), (tile_b_id, tile_b) = edge_list[i], edge_list[j]

            if tiles_fit(tile_a, tile_b):
                if tile_a_id in fitting_tiles:
                    fitting_tiles[tile_a_id].append(tile_b_id)
                else:
                    fitting_tiles[tile_a_id] = [tile_b_id]
                
                if tile_b_id in fitting_tiles:
                    fitting_tiles[tile_b_id].append(tile_a_id)
                else:
                    fitting_tiles[tile_b_id] = [tile_a_id]

    return fitting_tiles

def debug_edge_variations(image, edges):
    if len(edges) > 7:
        size = len(image)

        ascii_im = get_ascii_image(image, size)
        inital = get_ascii_edge_image(edges[0], size)
        hflip_inital = get_ascii_edge_image(edges[1], size)
        vflip_inital = get_ascii_edge_image(edges[2], size)
        rot1 = get_ascii_edge_image(edges[3], size)
        hflip_1 = get_ascii_edge_image(edges[4], size)
        vflip_1 = get_ascii_edge_image(edges[5], size)
        rot2 = get_ascii_edge_image(edges[6], size)
        rot3 = get_ascii_edge_image(edges[7], size)

        print('Image')
        for line in ascii_im:
            print(line)

        print('{:<{width}}  {:<{width}}  {:<{width}}  {:<{width}}'.format(
            'Inital', 'Rot1', 'Rot2', 'Rot3', width=size))
        for line in zip(inital, rot1, rot2, rot3):
            print('  '.join(line))

        print('Horizontal Flips')
        for line in zip(hflip_inital, hflip_1):
            print('  '.join(line))

        print('Vertical Flips')
        for line in zip(vflip_inital, vflip_1):
            print('  '.join(line))


def edge_variations(edges, size):
    top, right, bot, left = edges

    def reverse_bits(n, width):
        b = '{:0{width}b}'.format(n, width=width)
        return int(b[::-1], 2)

    result = [(top, right, bot, left)]      # inital orientation
    result.append((reverse_bits(top, size), left, reverse_bits(bot, size), right))  # horizontal flip 1/2
    result.append((bot, reverse_bits(right, size), top, reverse_bits(left, size)))  # vertical flip 1/2
    result.append((reverse_bits(left, size), top, reverse_bits(right, size), bot))  # rotate right 1/3
    result.append((left, bot, right, top))  # horizontal flip 2/2
    result.append((reverse_bits(right, size), reverse_bits(top, size), reverse_bits(left, size), reverse_bits(bot, size)))  # vertical flip 2/2
    result.append((reverse_bits(bot, size), reverse_bits(left, size), reverse_bits(top, size), reverse_bits(right, size)))  # rotate right 2/3
    result.append((right, reverse_bits(bot, size), left, reverse_bits(top, size)))  # rotate right 3/3

    return result


def parse_input(input):
    images, edges = {}, {}
    id, image = -1, []

    # add a empty line at the end
    input.append('')

    for line in input:
        id_match = re.match(r'Tile (\d+)', line)

        if not line and image:
            top, right, bot, left = image[0], 0, image[-1], 0

            for i, im in enumerate(image):
                left |= (im & 1) << i
                right |= ((im & (1 << (len(image) - 1)))
                          >> (len(image) - 1)) << i

            #print('l: {:010b} r: {:010b}'.format(left, right))

            images[id] = image
            edges[id] = edge_variations((top, right, bot, left), len(image))

            image = []
        elif id_match:
            id = int(id_match.group(1))
        else:
            image_line = 0

            for i, c in enumerate(line):
                if c == '#':
                    image_line |= 1 << i

            # print('{0:010b}'.format(image_line))

            image.append(image_line)

    return images, edges


def part_one(input):
    images, edges = parse_input(input)

    #debug_edge_variations(images[2953], edges[2953])
    fitting_tiles = get_fitting_tiles(edges)

    corner_pieces = map(lambda ft: ft[0], filter(lambda ft: len(ft[1]) == 2, fitting_tiles.items()))

    return reduce(lambda x, y: x * y, corner_pieces)


def part_two(input):
    return 0


def main():
    print('Day 20: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/input_day20.txt', '\n'))))
    print('Day 20: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/input_day20.txt', '\n'))))


if __name__ == "__main__":
    main()
