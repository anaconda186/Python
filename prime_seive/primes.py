import time


iterations = 1
length = 100000


def main():
    t = time.process_time()

    primes = [2, 3, 5, 7, 11, 13]
    current = 13
    threes_counter = 3
    sevens_counter = 4
    elevens_counter = 2
    thirteen_counter = 1

    while len(primes) < length:
        current += 2
        pass_number = False

        if threes_counter == 3:
            threes_counter = 1
            pass_number = True
        else:
            threes_counter += 1

        if sevens_counter == 7:
            sevens_counter = 1
            pass_number = True
        else:
            sevens_counter += 1

        if elevens_counter == 11:
            elevens_counter = 1
            pass_number = True
        else:
            elevens_counter += 1

        if thirteen_counter == 13:
            thirteen_counter = 1
            pass_number = True
        else:
            thirteen_counter += 1

        if int(repr(current)[-1]) == 5:
            pass_number = True

        if pass_number:
            continue

        append = True

        for e in primes[: round(len(primes) * (1 / 3))]:
            if current % e == 0:
                append = False
        if append:
            primes.append(current)
            print(f"{len(primes) / length * 100:.2f} %", end="\r")

    if primes[:10000] != known_primes[: len(primes[:10000])]:
        print("ERROR: The list of primes does not match known primes")
        exit(1)
    return time.process_time() - t


known_primes: list[int] = []
file = open("prime_list.txt", "r")
lines = file.readlines()
for line in lines:
    for number in line.split():
        known_primes.append(int(number))

metric = []
progress = 0
for _ in range(iterations):
    metric.append(main())
    progress += 1


metric.sort()
# print(metric[1:-1])
print(len(metric))
print(sum(metric) / len(metric))
