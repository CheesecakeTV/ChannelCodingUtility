from functools import lru_cache


@lru_cache()
def bin_len(theBin) -> int:
    counter = 0
    while theBin:
        counter += 1
        theBin >>= 1
    return counter

dasPoly = 0b1001011100111110
durch = 0b111

unterschied = bin_len(dasPoly) - bin_len(durch)
durch <<= unterschied
first_bit = 1 << bin_len(dasPoly) - 1

for i in range(unterschied + 1):
    print(bin(dasPoly))
    print(bin(durch))
    print()

    if first_bit & dasPoly:
        dasPoly ^= durch

    first_bit >>= 1
    durch >>= 1

print("Modulo:",bin(dasPoly))

