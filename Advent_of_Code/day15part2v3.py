import heapq
import time

start = time.perf_counter()
with open("list.txt", "r") as file:
    # Create number list

    distance_grid = []
    line = file.readline()
    while line:
        distance_grid.append([int(x) for x in line.strip("\n")])
        line = file.readline()

length_x = len(distance_grid)
length_y = len(distance_grid[0])

coordinates_dict = {}
for i in range(length_x * 5):
    m = i // length_x
    for j in range(length_y * 5):
        x = (i + 1) % length_x
        y = (j + 1) % length_y
        coordinates_dict[(i, j)] = distance_grid[x - 1][y - 1] + m + j // length_y
        if coordinates_dict[(i, j)] > 9:
            coordinates_dict[(i, j)] -= 9


# distance_grid = large_distance_grid
best_at_coord: dict[tuple[int, int], int] = {}
todo_list = [(0, (0, 0))]

while True:
    cost, coord = heapq.heappop(todo_list)

    # x = coord[0]
    # y = coord[1]
    if coord in best_at_coord and cost >= best_at_coord[coord]:
        continue
    else:
        best_at_coord[coord] = cost
    next_point = (
        (coord[0] + 1, coord[1]),
        (coord[0] - 1, coord[1]),
        (coord[0], coord[1] + 1),
        (coord[0], coord[1] - 1),
    )
    for spot in next_point:
        if spot in coordinates_dict:
            total_cost = cost + coordinates_dict[spot]
            heapq.heappush(todo_list, (total_cost, spot))

    if coord[0] == length_x * 5 - 1 and coord[1] == length_y * 5 - 1:
        break
print(f"{cost:04} | {coord[0]:3}, {coord[1]:3} | {time.perf_counter() - start:.2f}")
