


dasPoly = 0b_1001_0110_00
durch = 0b111

rem = 0

durch <<= 7
first_bit = 1 << 9

for i in range(8):
    print(bin(dasPoly))
    print(bin(durch))
    print()

    if first_bit & dasPoly:
        dasPoly ^= durch

    first_bit >>= 1
    durch >>= 1

