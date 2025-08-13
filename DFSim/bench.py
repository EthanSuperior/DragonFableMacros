def f_list(nodes):
    for n in nodes:
        pass


def f_tuple(nodes):
    for n in nodes:
        pass


def f_varargs(*nodes):
    for n in nodes:
        pass


import timeit

l1 = [1] * 500 
l2 = [2] * 500
l3 = [3] * 500

print("list:", timeit.timeit(lambda: f_list(l1 + l2 + l3), number=1000000))
print("tuple:", timeit.timeit(lambda: f_tuple(tuple(l1 + l2 + l3)), number=1000000))
print("varargs:", timeit.timeit(lambda: f_varargs(*l1, *l2, *l3)))
