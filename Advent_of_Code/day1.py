input_list = open("list.txt", "r")


increase = 0
x1 = 1000000
x2 = 1000000
x3 = 1000000
for line in input_list:
    y = int(line)
    if y > x1:
        increase += 1
    x1 = x2
    x2 = x3
    x3 = y


print(increase)
