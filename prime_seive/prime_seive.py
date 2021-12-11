import time

prime_list: list[int] = [2, 3, 5, 7]
length = 10 ** 6


k = 1
t = time.process_time()

while len(prime_list) < length:
    p = prime_list[k]
    q = prime_list[k + 1]
    segment = range(p * p, q * q, 2)
    for m in segment:
        append = True
        while append:
            for n in prime_list[: k + 1]:
                if m % n == 0:
                    append = False
                    break
            if append:
                # print(m)
                if len(prime_list) < length:
                    prime_list.append(m)
                break
    k += 1


print(
    f"Total time: {time.process_time() - t:2.2f}s \t| Prime/sec: {len(prime_list)/(time.process_time()-t+.0000001):.2f}/sec"
)

known_primes: list[int] = []
file = open("prime_list.txt", "r")
lines = file.readlines()
for line in lines:
    for number in line.split():
        known_primes.append(int(number))

if prime_list[:10000] != known_primes[: len(prime_list[:10000])]:
    print("ERROR: The list of primes does not match known primes")
    exit(1)
else:
    print("Prime check is true")
    print(len(prime_list))
