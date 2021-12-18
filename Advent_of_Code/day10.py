import statistics

with open("list.txt", "r") as file:
    diagnostic_list = []
    line = str(file.readline())
    while line:
        diagnostic_list.append(str(line).strip("\n"))
        line = str(file.readline())
score_map = {"(": 1, "[": 2, "{": 3, "<": 4}
char_map = {"(": ")", "[": "]", "{": "}", "<": ">"}
score = 0
score_list = []
for line in diagnostic_list:
    line_check = []
    line_list = list(line)
    append = True
    for char in line_list:
        if char in char_map:
            line_check.append(char)
        elif char == ")":
            if line_check[-1] == "(":
                line_check.pop()
            else:
                append = False
                break
        elif char == "]":
            if line_check[-1] == "[":
                line_check.pop()
            else:
                append = False
                break
        elif char == "}":
            if line_check[-1] == "{":
                line_check.pop()
            else:
                append = False
                break
        elif char == ">":
            if line_check[-1] == "<":
                line_check.pop()
            else:
                append = False
                break
    if append:
        score_list.append(line_check)

# Score list
new_score_list = []
for line in score_list:
    score = 0
    line = line[::-1]
    # print(line)
    for char in line:
        # print(char)
        score *= 5
        score += score_map[char]
    new_score_list.append(score)

# print(new_score_list)
# print(score_list)
print(statistics.median(new_score_list))
