import re
import math
import networkx as nx
from functools import reduce
import numpy as np
from src.common.util import read_input

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

def from_ascii(ascii):
    result = []

    for line in ascii:
        result_line = []
        for c in line:
            if c == '#':
                result_line.append(1)
            else:
                result_line.append(0)
        result.append(result_line)
        
    return result

def tiles_fit(tile_a, tile_b):
    # looks bad but is constant in n... 8 orientations for 4 edges ... 16 checks for one tile
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

def above(left, bottom, current):
    # check if current tile is above bottom using left as anchor
    for ol in left:
        _, lr, _, _ = ol
        for ob in bottom:
            bt, _, _, _ = ob
            for oc in current:
                _, _, cb, cl = oc
                if lr == cl and bt == cb:
                    return True
    return False

def get_corner(tiles, neighbors = []):
    # get a corner in the tile DS 
    # or if neighbors != [] get the corner which is next to a neighbor
    for tile, adjacent in tiles.items():
        if len(adjacent) == 2:
            if len(neighbors) > 0 and all(map(lambda t: t in adjacent, neighbors)):
                return tile
            else:
                return tile
    return None
        
def assemble(fitting_tiles, edges, size):
    tiles = dict(fitting_tiles) # local copy
    result = np.zeros((size, size))
    result_x, result_y = 0, 0
    stack = [get_corner(tiles)]

    while stack:
        if len(stack) > 1:
            tile_a, tile_b = stack.pop(), stack.pop()
            next, *_ = set(tiles[tile_a]) & set(tiles[tile_b])
            
            tile_a_above = above(edges[result[result_y][result_x - 1]], edges[next], edges[tile_a])
            tile_b_above = above(edges[result[result_y][result_x - 1]], edges[next], edges[tile_b])
            if not next:
                # no more elements in this row, continue with next one: y + 1
                stack.append(get_corner(tiles, result[result_y][0]))
                result_x, result_y = 0, result_y + 1
            else:
                stack.append(next)
        else:
            # current is a corner, get its neighbors
            current = stack.pop()

            stack += tiles[current]

            # update tile DS
            del tiles[current]
            for tile in stack:
                tiles[tile] = list(filter(lambda t: t != current, tiles[tile]))

            # place corner tile in result 
            result[result_y][result_x] = current
            result_x += 1

    return result 

def stich(images, order):
    image = []
    
    for i in range(10):
        line = []
        for o in order:
            current_line = images[o][i]

        image.append(line)

    return image

def match(image, pattern):
    result = 0
    return result

def part_one(input):
    images, edges = parse_input(input)

    fitting_tiles = get_fitting_tiles(edges)

    corner_pieces = map(lambda ft: ft[0], filter(lambda ft: len(ft[1]) == 2, fitting_tiles.items()))

    return reduce(lambda x, y: x * y, corner_pieces)


def part_two(input):
    images, edges = parse_input(input)
    pattern = from_ascii([
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '])
    
    fitting_tiles = get_fitting_tiles(edges)

    image_order = assemble(fitting_tiles, edges, int(math.sqrt(len(images))))

    image = stich(images, image_order)

    match_count = match(image, pattern)

    pattern_count = sum(map(lambda l: l.count(1), pattern))

    image_count = sum(map(lambda l: l.count(1), image))

    return image_count - (match_count * pattern_count)


def main():
    print('Day 20: Answer for Part 1 {}'.format(
        part_one(read_input('inputs/input_day20.txt', '\n'))))
    print('Day 20: Answer for Part 2: {}'.format(
        part_two(read_input('inputs/input_day20.txt', '\n'))))


if __name__ == "__main__":
    main()
