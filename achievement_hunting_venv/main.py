from game_library_functions import *
from game_class import Game

if __name__ == "__main__":

    # starting variables
    gamer = input("What is you Gamertag?").replace(" ", "+")
    ach_weights = 1.0
    ta_weights = 1.0
    gs_weights = 1.0
    weight_limit = 0.001
    precision = 4

    if gamer != "":
        game_library = get_game_list(gamer)
    else:
        game_library = get_game_list()

    # ACH weighting Loop #
    ach_weights = ach_weighting_loop(game_library, ach_weights, weight_limit, precision)

    # TA weighting Loop #
    ta_weights = ta_weighting_loop(game_library, ta_weights, weight_limit, precision)

    # Start GS weighting Loop #
    gs_weights = gs_weighting_loop(game_library, gs_weights, weight_limit, precision)

    # Alpha Values
    ach_alpha, ta_alpha, gs_alpha = alpha_values(
        game_library, ach_weights, ta_weights, gs_weights
    )

    # Create model group
    model_dict = {
        "ach_weights": ach_weights,
        "ach_alpha": ach_alpha,
        "ta_weights": ta_weights,
        "ta_alpha": ta_alpha,
        "gs_weights": gs_weights,
        "gs_alpha": gs_alpha,
    }

    # Establish predicted Values
    total_ach_gain, total_ta_gain, total_gs_gain = predict_gains(
        game_library, model_dict
    )

    game_library.sort(key=lambda x: x.predicted_gs_gains)
    print(game_library)
    print(
        f"ACH: M * {ach_weights} + {ach_alpha}, TA: M * {ta_weights} + {ta_alpha}, GS: M * {gs_weights} + {gs_alpha}"
    )
    print(
        f"Total Ach gain: {total_ach_gain}, Total TA gain: {total_ta_gain}, Total GS gain: {total_gs_gain}"
    )
