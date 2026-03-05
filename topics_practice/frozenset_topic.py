normal_set = {1, 2, 3, 3}
print("Normal set:", normal_set)

fs = frozenset([1, 2, 3, 4])
print("Frozenset:", fs)
print("Type of fs:", type(fs))

set_a = frozenset([1, 2, 3])
set_b = frozenset([3, 4, 5])

print("Union:", set_a | set_b)
print("Intersection:", set_a & set_b)
print("Is 2 in set_a:", 2 in set_a)

