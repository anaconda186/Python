import math

with open("list.txt", "r") as file:
    height_grid = []
    line = str(file.readline())
    while line:
        height_grid.append([int(x) for x in str(line).strip("\n")])
        line = str(file.readline())


def check_grid(x, y, height_grid, already_checked, basin_count):
    if [x, y] not in already_checked:
        already_checked.append([x, y])
        if height_grid[x][y] < 9:
            basin_count += 1
            # check not sides
            # if x does not equal 0,check the cell below it
            if x != 0:
                already_checked, basin_count = check_grid(
                    x - 1, y, height_grid, already_checked, basin_count
                )
            # if x does not equal max x,check the cell above it
            if x != len(height_grid) - 1:
                already_checked, basin_count = check_grid(
                    x + 1, y, height_grid, already_checked, basin_count
                )
            # if y does not  equal 0, check cell to the left
            if y != 0:
                already_checked, basin_count = check_grid(
                    x, y - 1, height_grid, already_checked, basin_count
                )
            # if y not equals max, check cell to right
            if y != len(height_grid[0]) - 1:
                already_checked, basin_count = check_grid(
                    x, y + 1, height_grid, already_checked, basin_count
                )

    return already_checked, basin_count


checked_corrdinates = []
basin_list = []
for i in range(len(height_grid)):
    for j in range(len(height_grid[0])):
        # start at lowest sport
        check_list = []

        basin_count = 0
        if i != 0:
            check_list.append(height_grid[i - 1][j])
        if i != len(height_grid) - 1:
            check_list.append(height_grid[i + 1][j])
        if j != 0:
            check_list.append(height_grid[i][j - 1])
        if j != len(height_grid[i]) - 1:
            check_list.append(height_grid[i][j + 1])
        if all(height_grid[i][j] < number for number in check_list):
            checked_corrdinates, basin_count = check_grid(
                i, j, height_grid, checked_corrdinates, basin_count
            )
            print(basin_count)
            # print(checked_corrdinates)
            basin_list.append(basin_count)
# print(height_grid)

top3 = sorted(basin_list, reverse=True)[:3]
print(top3)
print(math.prod(top3))
