from game_library_functions import *
from app import app
from curve_fit import *

if __name__ == "__main__":

    # starting variables
    gamer = input("What is you Gamertag?").replace(" ", "+")
    # ach_weights = 1.0
    # ta_weights = 1.0
    # gs_weights = 1.0
    # weight_limit = 0.001
    # precision = 9

    if gamer != "":
        game_library = get_game_list(gamer)
    else:
        game_library = get_game_list()

    # # ACH weighting Loop #
    # ach_weights = ach_weighting_loop(game_library, ach_weights, weight_limit, precision)

    # # TA weighting Loop #
    # ta_weights = ta_weighting_loop(game_library, ta_weights, weight_limit, precision)

    # # Start GS weighting Loop #
    # gs_weights = gs_weighting_loop(game_library, gs_weights, weight_limit, precision)

    # # Alpha Values
    # ach_alpha, ta_alpha, gs_alpha = alpha_values(
    #     game_library, ach_weights, ta_weights, gs_weights
    # )

    # # Create model group
    # model_dict = {
    #     "ach_weights": ach_weights,
    #     "ach_alpha": ach_alpha,
    #     "ta_weights": ta_weights,
    #     "ta_alpha": ta_alpha,
    #     "gs_weights": gs_weights,
    #     "gs_alpha": gs_alpha,
    # }

    # # Establish predicted Values
    # total_ach_gain, total_ta_gain, total_gs_gain = predict_gains(
    #     game_library, model_dict
    # )

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

    print(game_library)
    # print(
    #     f"ACH: M * {ach_weights} + {ach_alpha}, TA: M * {ta_weights} + {ta_alpha}, GS: M * {gs_weights} + {gs_alpha}"
    # )
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
