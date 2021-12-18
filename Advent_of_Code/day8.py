with open("list.txt", "r") as file:
    # Create number list
    key_list = []
    number_list = []
    line = file.readline()
    while line:
        key_list.append(line.strip("\n").split("|")[0])
        number_list.append(line.strip("\n").split("|")[1])
        line = file.readline()

# print(key_list, number_list)
count = 0
new_list = []
for key, number in zip(key_list, number_list):
    # print(key, number)
    key_list = {}
    segment_key = {}
    i = 0
    while len(key_list) < 10 and i < 100:
        # set key_list
        for key_word in key.split():
            sorted_word = sorted(key_word)
            word = "".join(sorted_word)
            # print(word)
            if len(word) == 2 and 1 not in key_list:
                key_list[1] = [char for char in word]
            if len(word) == 3 and 7 not in key_list:
                key_list[7] = [char for char in word]
            if len(word) == 4 and 4 not in key_list:
                key_list[4] = [char for char in word]
            if len(word) == 7 and 8 not in key_list:
                key_list[8] = [char for char in word]
            if (
                len(word) == 5
                and 1 in key_list
                and "bd" in segment_key
                and not all([character in word for character in key_list[1]])
                and not all([character in word for character in segment_key["bd"]])
            ):
                key_list[2] = [char for char in word]
            if (
                len(word) == 5
                and "b" in segment_key
                and "c" in segment_key
                and "f" in segment_key
                and not all([character in word for character in segment_key["b"]])
                and all([character in word for character in segment_key["c"]])
                and all([character in word for character in segment_key["f"]])
            ):
                key_list[3] = [char for char in word]
            if (
                len(word) == 5
                and "b" in segment_key
                and all([character in word for character in segment_key["b"]])
            ):
                key_list[5] = [char for char in word]
            if (
                len(word) == 6
                and "c" in segment_key
                and not all([character in word for character in segment_key["c"]])
            ):
                key_list[6] = [char for char in word]
            if (
                len(word) == 6
                and "d" in segment_key
                and not all([character in word for character in segment_key["d"]])
            ):
                key_list[0] = [char for char in word]
            if (
                len(word) == 6
                and "d" in segment_key
                and "c" in segment_key
                and all([character in word for character in segment_key["d"]])
                and all([character in word for character in segment_key["c"]])
            ):
                key_list[9] = [char for char in word]
            # print(key_list)
        # set Segment_key
        if 7 in key_list and 1 in key_list and not "a" in segment_key:
            segment_key["a"] = set(key_list[7]) - set(key_list[1])
        if 1 in key_list and not "cf" in segment_key:
            segment_key["cf"] = key_list[1]
        if 1 in key_list and 2 in key_list:
            segment_key["f"] = set(key_list[1]) - set(key_list[2])
        if 1 in key_list and "f" in segment_key:
            segment_key["c"] = set(key_list[1]) - set(segment_key["f"])
        if 4 in key_list and 1 in key_list and not "bd" in segment_key:
            segment_key["bd"] = set(key_list[4]) - set(key_list[1])
        if 2 in key_list and "bd" in segment_key:
            segment_key["b"] = set(segment_key["bd"]) - set(key_list[2])
        if "b" in segment_key and "bd" in segment_key:
            segment_key["d"] = set(segment_key["bd"]) - set(segment_key["b"])

        # print(segment_key)
        i += 1
    # print(key_list, segment_key)

    number_string = ""
    for word in number.split():
        print(word)
        word = sorted(word)
        if word == key_list[0]:
            number_string += str(0)
        elif word == key_list[1]:
            number_string += str(1)
        elif word == key_list[2]:
            number_string += str(2)
        elif word == key_list[3]:
            number_string += str(3)
        elif word == key_list[4]:
            number_string += str(4)
        elif word == key_list[5]:
            number_string += str(5)
        elif word == key_list[6]:
            number_string += str(6)
        elif word == key_list[7]:
            number_string += str(7)
        elif word == key_list[8]:
            number_string += str(8)
        elif word == key_list[9]:
            number_string += str(9)
        else:
            print("Error:", word)
    print(number_string)
    count += int(number_string)
print(count)
