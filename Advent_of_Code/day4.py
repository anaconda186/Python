# Read input file


with open("list.txt", "r") as file:

    # Create number list
    number_list = [int(x) for x in file.readline().strip("\n").split(",")]

    # Create Board List
    board_list = []

    while file.readline():

        card_line = []
        for i in range(5):
            card_line.extend(
                [int(x) for x in file.readline().strip("\n").split(" ") if x != ""]
            )
        board_list.append(card_line)


# Define check board function
def check_winner(card):
    # horizontal winner
    start = 0
    horizontal = 0
    for i in range(5):
        for j in range(5):
            horizontal += card[start + j]
        if horizontal == 5000:

            return True
        start += 5
        horizontal = 0

    # Vertical winner
    start = 0
    vertical = 0
    for i in range(5):
        for j in range(5):
            vertical += card[start + (j * 5)]
        if vertical == 5000:

            return True
        start += 1
        vertical = 0
    return False


# Define remove number function
winner = False
i = 0
while len(board_list) > 0:
    picked_number = number_list[i]
    for j in range(len(board_list)):
        for k in range(25):
            if board_list[j][k] == picked_number:
                board_list[j][k] = 1000
    new_board_list = []
    for board in board_list:
        if not check_winner(board):
            new_board_list.append(board)
    if len(new_board_list) == 0:
        break

    i += 1

    board_list = new_board_list.copy()

print(board_list)
print(picked_number)
print(sum(board_list[0]))
x = board_list[0].count(1000)
print(x)
print(sum(board_list[0]) - (x * 1000))
print(picked_number * (sum(board_list[0]) - (x * 1000)))
