import heapq
import time


with open("list.txt", "r") as file:
    # Create number list

    distance_grid = []
    line = file.readline()
    while line:
        distance_grid.append([int(x) for x in line.strip("\n")])
        line = file.readline()

large_distance_grid = [
    [0] * (len(distance_grid) * 5) for i in range(len(distance_grid[0]) * 5)
]
for i in range(len(large_distance_grid)):
    m = i // len(distance_grid)
    for j in range(len(large_distance_grid)):
        x = (i + 1) % len(distance_grid)
        y = (j + 1) % len(distance_grid[0])
        large_distance_grid[i][j] = (
            distance_grid[x - 1][y - 1] + m + j // len(distance_grid[0])
        )
        if large_distance_grid[i][j] > 9:
            large_distance_grid[i][j] -= 9

# print(large_distance_grid)
distance_grid = large_distance_grid
# total_distance_grid = [
#     [100000000] * (len(distance_grid)) for i in range(len(distance_grid[0]))
# ]
best_at_coord = {}

# visited = []
# unvisited = {
#     (0, 0): 0,
#     (0, 1): 100000000,
#     (1, 0): 100000000,
# }
todo_list = [(0, (0, 0))]
# for i in range(len(total_distance_grid)):
#     for j in range(len(total_distance_grid[i])):
#         unvisited[i, j] = total_distance_grid[i][j]

# print(distance_grid)
# total_distance_grid[0][0] = 0

# print(total_distance_grid)


# def find_next_spot(unvisited):
#     coord = min(unvisited, key=unvisited.get)
#     x = coord[0]
#     y = coord[1]
#     print(unvisited[coord], coord)
#     return x, y


# x = 0
# y = 0
start = time.perf_counter()
while True:
    cost, coord = heapq.heappop(todo_list)
    print(f"{cost:04} | {coord[0]:3}, {coord[1]:3} | {time.perf_counter() - start:.2f}")
    x = coord[0]
    y = coord[1]
    if (x, y) in best_at_coord and cost >= best_at_coord[(x, y)]:
        continue
    else:
        best_at_coord[(x, y)] = cost

    for k, l in zip([1, -1, 0, 0], [0, 0, 1, -1]):
        if (
            x + k >= 0
            and y + l >= 0
            and x + k <= len(distance_grid) - 1
            and y + l <= len(distance_grid[0]) - 1
        ):
            total_cost = cost + distance_grid[x + k][y + l]
            heapq.heappush(
                todo_list, (cost + distance_grid[x + k][y + l], (x + k, y + l))
            )
    # print(distance_grid)
    # print(total_distance_grid)
    # x, y = find_next_spot(unvisited)
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
