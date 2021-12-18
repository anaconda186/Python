with open("list.txt", "r") as file:
    # Create number list

    distance_grid = []
    line = file.readline()
    while line:
        distance_grid.append([int(x) for x in line.strip("\n")])
        line = file.readline()


total_distance_grid = [
    [100000000] * (len(distance_grid)) for i in range(len(distance_grid[0]))
]

unvisited = []
for i in range(len(total_distance_grid)):
    for j in range(len(total_distance_grid[i])):
        unvisited.append([i, j])

print(distance_grid)
total_distance_grid[0][0] = distance_grid[0][0]
print(total_distance_grid)


def update_neighbors(i, j):
    unvisited.remove([i, j])
    for k, l in zip([1, -1, 0, 0], [0, 0, 1, -1]):
        if (
            i + k >= 0
            and j + l >= 0
            and i + k <= len(distance_grid) - 1
            and j + l <= len(distance_grid[0]) - 1
        ):
            if [i + k, j + l] in unvisited and total_distance_grid[i + k][j + l] > (
                total_distance_grid[i][j] + distance_grid[i + k][j + l]
            ):
                total_distance_grid[i + k][j + l] = (
                    total_distance_grid[i][j] + distance_grid[i + k][j + l]
                )


def find_next_spot(total_distance_grid, unvisited):
    lowest_spot = 100000000
    x = 0
    y = 0
    for spot in unvisited:
        i = spot[0]
        j = spot[1]
        if total_distance_grid[i][j] < lowest_spot:
            lowest_spot = total_distance_grid[i][j]
            x = i
            y = j
    print(lowest_spot, x, y)
    return x, y


x = 0
y = 0

while True:
    update_neighbors(x, y)
    # print(distance_grid)
    # print(total_distance_grid)
    x, y = find_next_spot(total_distance_grid, unvisited)
    # print(x, y)
    if x == len(distance_grid) - 1 and y == len(distance_grid[0]) - 1:
        break


# def pathfinding(starting_point, current_path, current_distance, best_distance):
#     i = starting_point[0]
#     j = starting_point[1]
#     for k in [-1, 0, 1]:
#         for l in [-1, 0, 1]:
#             if (
#                 [i + k, j + l] not in current_path
#                 and i + k >= 0
#                 and j + l >= 0
#                 and i + k <= len(grid) - 1
#                 and j + l <= len(grid[0]) - 1
#             ):
#                 current_path.append([i + k, j + l])
#                 current_distance += grid[i + k][j + l]
#                 if i + k == len(grid) - 1 and j + l == len(grid[0]) - 1:
#                     if current_distance < best_distance:
#                         best_distance = current_distance
#                         best_path = current_path
#                         print(best_distance, best_path)
#                 else:
#                     pathfinding(
#                         [i + k, j + l], current_path, current_distance, best_distance
#                     )
#                 current_path.pop()
#                 current_distance -= grid[i + k][j + l]


# best_path = []
# best_distance = 1000000000
# current_distance = 0
# current_path = []
# pathfinding([0, 0], current_path, current_distance, best_distance)

# print(best_distance, best_path)
