with open("list.txt", "r") as file:
    glow_grid = []
    line = str(file.readline())
    while line:
        glow_grid.append([int(x) for x in str(line).strip("\n")])
        line = str(file.readline())

print(glow_grid)
count = 0
failed = True
while failed:
    for i in range(len(glow_grid)):
        for j in range(len(glow_grid[i])):
            glow_grid[i][j] += 1

    flashed = []
    hold_step = True
    while hold_step:
        hold_step = False
        for i in range(len(glow_grid)):
            for j in range(len(glow_grid[i])):
                if glow_grid[i][j] == 10:
                    flashed.append([i, j])
                    glow_grid[i][j] = 0

                    for k in [-1, 0, 1]:
                        for l in [-1, 0, 1]:
                            if (
                                [i + k, j + l] not in flashed
                                and i + k >= 0
                                and j + l >= 0
                                and i + k <= len(glow_grid) - 1
                                and j + l <= len(glow_grid[0]) - 1
                            ):
                                glow_grid[i + k][j + l] = min(
                                    10, glow_grid[i + k][j + l] + 1
                                )
                                hold_step = True
    count += 1
    failed = False
    for i in range(len(glow_grid)):
        for j in range(len(glow_grid[i])):
            if glow_grid[i][j] != 0:
                failed = True

    print(glow_grid)
    print(count)
    # input("continue?")
