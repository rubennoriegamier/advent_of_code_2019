from itertools import accumulate, chain, cycle, islice, repeat
from operator import mul

BASE_PATTERN = 0, 1, 0, -1


def main():
    signal = list(map(int, input().rstrip()))
    fft = fft_1(signal)
    print(*next(islice(fft, 99, None))[:8], sep='')
    fft = fft_2(signal, 10_000)
    print(*next(islice(fft, 99, None))[:8], sep='')


def fft_1(signal):
    patterns = []
    for n in range(1, len(signal) + 1):
        pattern_cycle = cycle(chain.from_iterable(repeat(pattern_digit, n) for pattern_digit in BASE_PATTERN))
        pattern = list(islice(pattern_cycle, n, len(signal) + 1))
        while pattern[-1] == 0:
            pattern.pop()
        patterns.append(pattern)
    while True:
        signal = [abs(sum(map(mul, islice(signal, index, None), patterns[index]))) % 10 for index in range(len(signal))]
        yield signal


def fft_2(signal, multiplier):
    offset = int(''.join(map(str, signal[:7])))
    signal = list(islice(chain(islice(signal, offset % len(signal), None),
                               cycle(signal)),
                         0, len(signal) * multiplier - offset))
    while True:
        signal.reverse()
        signal = [n % 10 for n in accumulate(signal)]
        signal.reverse()
        yield signal


if __name__ == '__main__':
    main()
