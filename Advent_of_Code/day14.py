from collections import defaultdict

with open("list.txt", "r") as file:
    # Create number list

    starting_string = file.readline().strip("\n")
    file.readline()
    instructions = {}
    line = file.readline()
    while line:
        instructions[line.split(" -> ")[0]] = line.strip("\n").split(" -> ")[1]
        line = file.readline()

# print(starting_string)
print(instructions)
print(len(instructions))

count_map = {}
for key in instructions:
    count_map[key] = 0
    count_map
# print(count_map)

# start polymer
for i in range((len(starting_string) - 1)):
    current_chain = starting_string[i] + starting_string[i + 1]
    count_map[current_chain] += 1

# print(count_map)

# grow polymer

for _ in range(100):
    new_chain_count = defaultdict(int)
    print(new_chain_count)
    for link in count_map:
        middle_link = instructions[link]
        count = count_map[link]
        ab = link[0] + middle_link
        bc = middle_link + link[1]
        new_chain_count[ab] += count
        new_chain_count[bc] += count
    count_map = new_chain_count.copy()
    print(new_chain_count)
    print(count_map)
    total_count = defaultdict(int)
    for link in count_map:
        total_count[link[1]] += count_map[link]
    total_count["N"] += 1
    print(total_count)
    print(max(total_count.values()) - min(total_count.values()))
