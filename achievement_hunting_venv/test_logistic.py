logistic_ach_weights = [0.0, 1.0, 0.5, 1.0, 1.0]

exponent = -1

# while exponent >= -4:
logistic_test_ach_list = [[logistic_ach_weights] for i in range(15)]
for i in range(len(logistic_ach_weights)):
    logistic_test_ach_list[i * 3][i] = logistic_ach_weights[i]
    logistic_test_ach_list[i * 3 + 1][i] = logistic_ach_weights[i] + (10 ** exponent)
    logistic_test_ach_list[i * 3 + 2][i] = logistic_ach_weights[i] - (10 ** exponent)

print(logistic_test_ach_list)
