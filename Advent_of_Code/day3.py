input_list = open("list.txt", "r")
new_list = []
for line in input_list:
    new_list.append(line)


def sum_binary(input, digit):
    ones = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    zeroes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for line in input:
        for i in range(0, len(str(line.strip("\n")))):
            if int(line[i]) == 1:
                ones[i] += 1
            else:
                zeroes[i] += 1
    print(ones, zeroes)
    if ones[digit] < zeroes[digit]:
        return 1
    else:
        return 0


for j in range(0, 12):
    x = sum_binary(new_list, j)
    interim_list = []
    for line in new_list:
        if int(line[j]) == x:
            interim_list.append(line)
    new_list = interim_list.copy()
    print(new_list)
    if len(new_list) == 1:
        break

oxygen = int(new_list[0], 2)
print(oxygen)
