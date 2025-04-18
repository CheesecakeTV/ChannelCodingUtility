from functools import lru_cache
import random as r

@lru_cache()
def bin_len(theBin) -> int:
    counter = 0
    while theBin:
        counter += 1
        theBin >>= 1
    return counter

# data = [
#     0b10010111,
#     0b00111110,
#     0b10010111,
#     0b00111110,
#     0
# ]

data = [r.randint(0,255) for _ in range(100)] + [0]

gen = 0b10000111

print("Data-stream:",bin(sum([
    i << 8 * n for n,i in enumerate(data[::-1])
])))
print("Generator:",bin(gen))

def poly_mod(dasPoly,durch):

    durch <<= 8
    first_bit = 1 << 15

    for i in range(9):
        # print(bin(dasPoly))
        # print(bin(durch))
        # print(bin(first_bit))
        # print()

        if first_bit & dasPoly:
            dasPoly ^= durch

        first_bit >>= 1
        durch >>= 1

    return dasPoly

mod = data[0]
for i in data[1:]:
    nextNum = (mod << 8) + i
    nextNum &= (1 << 16) - 1
    mod = poly_mod(nextNum, gen)

print("Modulo:",bin(mod))


