print("Flow control examples")

num = 7
if num > 0:
    print("Positive number")
elif num == 0:
    print("Zero")
else:
    print("Negative number")

# even or odd (from readme list)
n = 10
if n % 2 == 0:
    print(n, "is even")
else:
    print(n, "is odd")

print("Numbers from 1 to 5:")
for i in range(1, 6):
    print(i)

print("While loop from 1 to 5:")
i = 1
while i <= 5:
    print(i)
    i = i + 1

