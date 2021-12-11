input_list = open("list.txt", "r")

horizontal = 0
vertical = 0
aim = 0
for line in input_list:
    command = line.split()[0]
    amount = int(line.split()[1])
    if command == "forward":
        horizontal += amount
        vertical += aim * amount
        vertical = max(vertical, 0)
    if command == "up":
        aim -= amount

    if command == "down":
        aim += amount


print(horizontal)
print(vertical)
print(vertical * horizontal)
