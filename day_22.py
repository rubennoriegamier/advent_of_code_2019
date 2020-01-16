import fileinput
import re


def main():
    techniques = tuple(Shuffler.parse_techniques(map(str.rstrip, fileinput.input())))
    print(part_1(techniques))


def part_1(techniques):
    shuffler = Shuffler(10_007, techniques)
    return list(shuffler.positions(2019))[-1]


class Shuffler:
    __slots__ = '_deck_size', '_techniques'

    def __init__(self, deck_size, techniques):
        self._deck_size = deck_size
        self._techniques = tuple(techniques)

    def positions(self, position):
        for technique, n in self._techniques:
            if technique == 0:
                position = self._deck_size - position - 1
            elif technique == 1:
                position = (position - n) % self._deck_size
            elif technique == 2:
                position = position * n % self._deck_size
            yield position

    @staticmethod
    def parse_techniques(lines):
        cut = re.compile('cut (-?\\d+)')
        increment = re.compile('deal with increment (-?\\d+)')
        for line in lines:
            if line == 'deal into new stack':
                yield 0, -1
            else:
                cut_match = cut.fullmatch(line)
                if cut_match:
                    yield 1, int(cut_match.group(1))
                increment_match = increment.fullmatch(line)
                if increment_match:
                    yield 2, int(increment_match.group(1))


if __name__ == '__main__':
    main()
