from functools import partial
from itertools import dropwhile
from operator import eq

IMAGE_HEIGHT = 6
IMAGE_WIDTH = 25


def main():
    layers = extract_layers(input().rstrip())
    print(part_1(layers))
    print(part_2(layers))


def split_in_groups_of(sequence, n):
    return (sequence[i:i + n] for i in range(0, len(sequence), n))


def extract_layers(image):
    return tuple(split_in_groups_of(image, IMAGE_HEIGHT * IMAGE_WIDTH))


def part_1(layers):
    layer = min(layers, key=lambda layer_: sum(map(partial(eq, '0'), layer_)))
    count_1 = sum(map('1'.__eq__, layer))
    count_2 = sum(map('2'.__eq__, layer))
    return count_1 * count_2


def part_2(layers):
    colors = {'0': ' ', '1': '■'}
    return '\n'.join(split_in_groups_of(''.join(map(colors.get,
                                                    map(next,
                                                        map(partial(dropwhile, '2'.__eq__),
                                                            zip(*layers))))),
                                        IMAGE_WIDTH))


if __name__ == '__main__':
    main()
