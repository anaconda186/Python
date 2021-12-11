coordinates = []
with open("list.txt", "r") as file:
    for line in file:
        start, end = line.strip().split(" -> ")
        print(start, end)
        coordinates.append([start.split(","), end.split(",")])

print(coordinates)

grid = [[0] * 1000 for i in range(1000)]

for pair in coordinates:

    x1 = int(pair[0][0])
    y1 = int(pair[0][1])
    x2 = int(pair[1][0])
    y2 = int(pair[1][1])
    # if X's are the same, pair is vertical
    if x1 == x2:
        top = min(y1, y2)
        bot = max(y1, y2)
        for index in range(int(top), int(bot) + 1):
            grid[index][x1] += 1

    # if Y's are the same, pair is horizontal
    elif y1 == y2:
        lef = min(x1, x2)
        rig = max(x1, x2)
        for index in range(int(lef), int(rig) + 1):
            grid[y1][index] += 1
    # move lowest x to position 0
    else:
        if x1 > x2:
            x1, y1, x2, y2 = x2, y2, x1, y1
        # x is now always moving right test y is rising

        current_x = x1
        current_y = y1
        if y1 > y2:
            while current_x != x2 + 1 and current_y != y2 - 1:
                grid[current_y][current_x] += 1
                current_x += 1
                current_y -= 1
        elif y1 < y2:
            while current_x != x2 + 1 and current_y != y2 + 1:
                grid[current_y][current_x] += 1
                current_x += 1
                current_y += 1


# print(grid)
count = 0
for row in grid:
    for column in row:
        if column >= 2:
            count += 1

print(count)
