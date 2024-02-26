import os

path = os.path.realpath("new.txt")
print(path)
print(os.path.exists("new.txt"))

if not os.path.exists("new.txt"):
    with open("new.txt", "w", encoding="utf-8") as test_file:
        test_file.write("test;file").close() # Close redundant using "with open"

read_file = open("new.txt", "r")
lines = read_file.readlines()

for line in lines:
    print(line, end="")