from cs50 import get_float

while True:
        change = get_float("Change: ")
        if change > 0:
                break

change = int(round(change * 100)) # floats have imprecision --> change to int
count = 0

if change >= 25:
        while change >= 25:
                change -= 25
                count += 1
if change < 25 and change >= 10:
        while change >= 10:
                change -= 10
                count += 1
if change < 10 and change >= 5:
        while change >= 5:
                change -= 5
                count += 1
if change < 5 and change >= 1:
        while change >= 1:
                change -= 1
                count += 1

print(f"{count}")

