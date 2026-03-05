text = "hello world"
print("Original:", text)
print("Length:", len(text))
print("Upper:", text.upper())
print("Lower:", text.lower())
print("First 5 characters:", text[0:5])

# reverse a string (from readme)
name = "dhanush"
rev = name[::-1]
print("Name:", name)
print("Reversed name:", rev)

# check palindrome
word = "madam"
if word == word[::-1]:
    print(word, "is palindrome")
else:
    print(word, "is not palindrome")

# count vowels
sentence = "this is a simple string"
vowels = "aeiou"
count = 0
for ch in sentence:
    if ch in vowels:
        count = count + 1
print("Sentence:", sentence)
print("Vowel count:", count)

