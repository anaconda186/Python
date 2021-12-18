with open("list.txt", "r") as file:
    # Create number list
    number_list = [int(x) for x in file.readline().strip("\n").split(",")]
number_list.sort()
print(sum(number_list) / len(number_list))

best_option = 10 ** 15
best_coordinate = 0
for i in range(0, 1000):
    total_fuel = 0
    for crab in number_list:
        for j in range(1, abs(crab - i) + 1):
            total_fuel += j
    if total_fuel < best_option:
        best_option = total_fuel
        best_coordinate = i
    print(i)

print(best_coordinate)

print(best_option)
