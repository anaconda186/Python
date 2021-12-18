import time

from curve_fit import logit_curve_fit
from game_library_functions import (
    get_curve_fit_xy,
    get_game_list,
    norm_gains,
    predict_logistic_gains,
)


def achievements():

    # starting variables
    # gamer = input("What is you Gamertag?").replace(" ", "+")
    gamer = "Acidreactive"

    t = time.perf_counter()

    if gamer != "":
        game_library = get_game_list(gamer)
    else:
        game_library = get_game_list()

    # Get XY vaules
    xy_values = get_curve_fit_xy(game_library)

    # Call Curve_fit
    constants = logit_curve_fit(xy_values)

    # Establish Predicted Logistic Values
    total_ach_gain, total_ta_gain, total_gs_gain = predict_logistic_gains(
        game_library, constants
    )

    # Normalize gains
    norm_gains(game_library)

    # Sort Game library
    game_library.sort(key=lambda x: x.total_norm_value)

    print(game_library[-10:])
    print("\n")
    print(
        f"Total Ach gain: {total_ach_gain:.0f}, Total TA gain: {total_ta_gain:.0f}, Total GS gain: {total_gs_gain:.0f}, Game Count : {len(game_library)}"
    )
    print("\n")
    print(
        f"ACH | a: {constants[0][0]:.5f}, b: {constants[0][1]:.5f}, c: {constants[0][2]:.5f}, d: {constants[0][3]:.5f}, g:{constants[0][4]:.5f}"
    )
    print(
        f"TA  | a: {constants[1][0]:.5f}, b: {constants[1][1]:.5f}, c: {constants[1][2]:.5f}, d: {constants[1][3]:.5f}, g:{constants[1][4]:.5f}"
    )
    print(
        f"GS  | a: {constants[2][0]:.5f}, b: {constants[2][1]:.5f}, c: {constants[2][2]:.5f}, d: {constants[2][3]:.5f}, g:{constants[2][4]:.5f}"
    )

    print(f"{(time.perf_counter() - t):.5f}", "s")


if __name__ == "__main__":
    achievements()
