# [y for y in self.books_list if y[0] not in self.issued_list[0]]
import random

y = [(4, 2)]

z = [(1, 2), (4, 5)]


def gen_uid():
    return random.randrange(1000000000, 9999999999)


for x in range(20):
    print(gen_uid())
