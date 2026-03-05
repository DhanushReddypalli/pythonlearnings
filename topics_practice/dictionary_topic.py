student = {"name": "dhanush", "age": 25, "course": "python"}
print("Student dict:", student)
print("Name:", student["name"])
print("Age:", student.get("age"))

student["age"] = 26
print("After updating age:", student)

student["city"] = "Bengaluru"
print("After adding city:", student)

if "course" in student:
    print("Course key exists")

for key in student:
    print("Key:", key, "Value:", student[key])

# dictionary from two lists
keys = ["a", "b", "c"]
values = [1, 2, 3]
new_dict = dict(zip(keys, values))
print("New dict from lists:", new_dict)

