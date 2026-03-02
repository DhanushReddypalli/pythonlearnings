
person = ("dhanush", 25, "Developer")
print("Tuple:", person)
 

print("Type:", type(person))
 

print("Name:", person[0])
print("Age:", person[1])
print("Profession:", person[-1])
 

print("Slice (0 to 2):", person[0:2])

packed = "dhanush", "Python", "India"
print("Packed Tuple:", packed)
 

name, skill, country = packed
print("Unpacked values:")
print("Name:", name)
print("Skill:", skill)
print("Country:", country)
 

single_name = ("dhanush",)
print("Single element tuple:", single_name)
print("Type of single element tuple:", type(single_name))
 