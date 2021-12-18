with open("list.txt", "r") as file:
    # Create number list
    dots = []
    instruction = []
    line = file.readline()
    while line:
        if line.startswith("fold"):
            instruction.append(line.strip("\n").split(" ")[2])
        else:
            dots.append(line.strip("\n"))
        line = file.readline()
dots.pop()
print(dots)
print(instruction)


def print_points(grid):
    for i in range(len(grid)):
        for j in grid[i]:
            if j == " ":
                print(" ", end="")
            else:
                print("#", end="")
        print("\n", end="")


x_coordinate = []
y_coordinate = []
for dot in dots:
    x_coordinate.append(int(dot.split(",")[0]))
    y_coordinate.append(int(dot.split(",")[1]))

print(x_coordinate)
print(y_coordinate)
# create dot grid
grid = [[" "] * (max(x_coordinate) + 1) for i in range(max(y_coordinate) + 1)]

for x, y in zip(x_coordinate, y_coordinate):
    grid[y][x] = "X"
# print_points(grid)

for fold in instruction:
    new_x_coordinates = []
    new_y_coordinates = []
    axis = fold.split("=")[0]
    vertice = int(fold.split("=")[-1])
    if axis == "y":
        for x, y in zip(x_coordinate, y_coordinate):
            new_x_coordinates.append(x)
            if y > vertice:
                new_y = (2 * vertice) - y
                new_y_coordinates.append(new_y)
            else:
                new_y_coordinates.append(y)

    else:
        for x, y in zip(x_coordinate, y_coordinate):
            new_y_coordinates.append(y)
            if x > vertice:
                new_x = (2 * vertice) - x
                new_x_coordinates.append(new_x)
            else:
                new_x_coordinates.append(x)
    x_coordinate = new_x_coordinates.copy()
    y_coordinate = new_y_coordinates.copy()
    grid = [[" "] * (max(x_coordinate) + 1) for i in range(max(y_coordinate) + 1)]

    for x, y in zip(x_coordinate, y_coordinate):
        grid[y][x] = "X"
    count = 0
    for i in range(len(grid)):
        for j in grid[i]:
            if j == "X":
                count += 1

    print(f"current count: {count}")
print_points(grid)
