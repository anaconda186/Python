with open("list.txt", "r") as file:
    # Create number list
    start = []
    end = []
    line = file.readline()
    while line:
        start.append(line.strip("\n").split("-")[0])
        end.append(line.strip("\n").split("-")[1])
        line = file.readline()

# construct map dictionairy
map_connections = {}

for start, end in zip(start, end):
    # print(start, end)
    if start in map_connections:
        map_connections[start].append(end)
    else:
        map_connections[start] = [end]
    if end in map_connections:
        map_connections[end].append(start)
    else:
        map_connections[end] = [start]

# print(map_connections)
path_count = 0
current_path = []
# path_list = []
small_cave_count = {}


def next_step(
    starting_point: str,
    map_dict: dict,
    current_path: list,
    cave_count: dict,
    path_count: int,
):
    current_path.append(starting_point)
    if starting_point.islower():
        if starting_point in cave_count:
            cave_count[starting_point] += 1
        else:
            cave_count[starting_point] = 1
    if starting_point == "end":
        # path_list.append(current_path.copy())
        path_count += 1
        # print(current_path)
    else:
        for path in map_dict[starting_point]:
            if path != "start":
                if path.islower() and (
                    path not in current_path or max(cave_count.values()) < 2
                ):
                    path_count = next_step(
                        path, map_dict, current_path, small_cave_count, path_count
                    )
                    current_path.pop()
                    cave_count[path] -= 1
                if path.isupper():
                    path_count = next_step(
                        path, map_dict, current_path, small_cave_count, path_count
                    )
                    current_path.pop()
    return path_count


path_count = next_step(
    "start", map_connections, current_path, small_cave_count, path_count
)
# print(path_list)
print(path_count)
