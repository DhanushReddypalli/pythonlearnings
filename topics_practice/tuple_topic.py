person = ("dhanush", 25, "Developer")
print("Tuple:", person)
print("Type:", type(person))

print("Name:", person[0])
print("Age:", person[1])
print("Profession:", person[2])

print("Slice 0 to 2:", person[0:2])

packed = "python", "india", 2024
print("Packed tuple:", packed)

name, country, year = packed
print("Unpacked name:", name)
print("Unpacked country:", country)
print("Unpacked year:", year)

single = ("only_one",)
print("Single element tuple:", single)
print("Single element type:", type(single))

