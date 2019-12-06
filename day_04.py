def main():
    min_value, max_value = map(int, input().split('-'))
    print(*different_passwords(min_value, max_value), sep='\n')


def different_passwords(min_value, max_value):
    min_value_digits = list(map(int, str(min_value)))
    max_value_digits = list(map(int, str(max_value)))
    count_part_1 = 0
    count_part_2 = 0
    for a in range(min_value_digits[0], max_value_digits[0] + 1):
        for b in range(a, 10):
            for c in range(b, 10):
                for d in range(c, 10):
                    for e in range(d, 10):
                        for f in range(e, 10):
                            if ((a == b or b == c or c == d or d == e or e == f) and
                                    min_value_digits <= [a, b, c, d, e, f] <= max_value_digits):
                                count_part_1 += 1
                                if (a == b and b != c or
                                        b == c and a != b and c != d or
                                        c == d and b != c and d != e or
                                        d == e and c != d and e != f or
                                        e == f and d != e):
                                    count_part_2 += 1
    return count_part_1, count_part_2


if __name__ == '__main__':
    main()
