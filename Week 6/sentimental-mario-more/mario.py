from cs50 import get_int
height = 0

while height <= 0 or height > 8:
    height = get_int("Height: ")

for i in range(height):
    for space in range(height - i - 1):
        print(" ", end="")
    for left in range(i+1):
        print("#", end="")
    for gap in range(2):
        print(" ", end="")
    for right in range(i+1):
        print("#", end="")
    print("")
