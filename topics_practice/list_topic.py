numbers = [5, 2, 9, 1, 5]
print("List:", numbers)
print("First element:", numbers[0])
print("Last element:", numbers[-1])

# sum of list
total = 0
for n in numbers:
    total = total + n
print("Sum of list:", total)

# largest and smallest (from readme ideas)
print("Max using built-in:", max(numbers))
print("Min using built-in:", min(numbers))

# remove duplicates using set
unique = list(set(numbers))
print("Unique values:", unique)

# list comprehension (simple example)
squares = [n * n for n in range(1, 6)]
print("Squares 1 to 5:", squares)

