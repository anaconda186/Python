import requests
from bs4 import BeautifulSoup
from game_class import Game


def get_game_list(gamer: str = "Acidreactive") -> list:

    user = gamer
    r = requests.get(
        f"https://www.trueachievements.com/gamer/{user}/games?oGamerGamesList_ShowAll=True"
    ).text

    soup = BeautifulSoup(r, "html.parser")

    game_library = []

    for game in soup.findAll("tr", class_=("even", "odd", "green")):

        if (
            int(
                game.select("td:nth-of-type(5)")[0]
                .text.split(" ")[2]
                .replace(",", "")
                .replace("(", "")
                .replace(")", "")
            )
            == 0
        ):
            continue
        game = Game(game)
        game_library.append(game)

    return game_library


def ach_weighting_loop(
    game_library: list, ach_weights: float, weight_limit: float, precision: int
) -> float:
    exponent = -1
    while exponent >= -precision:
        prop_pos_ach_weights = ach_weights + (10 ** exponent)
        prop_neg_ach_weights = ach_weights - (10 ** exponent)
        current_ach_sum = 0.0
        prop_pos_ach_sum = 0.0
        prop_neg_ach_sum = 0.0
        for game in game_library:
            game.update_ach_weights(ach_weights, weight_limit)
            current_ach_sum += game.ach_weight * (
                abs(game.ach_ratio - (game.total_difficulty * ach_weights)) ** 2
            )
            game.update_ach_weights(prop_pos_ach_weights, weight_limit)
            prop_pos_ach_sum += game.ach_weight * (
                abs(game.ach_ratio - (game.total_difficulty * prop_pos_ach_weights))
                ** 2
            )
            game.update_ach_weights(prop_neg_ach_weights, weight_limit)
            prop_neg_ach_sum += game.ach_weight * (
                abs(game.ach_ratio - (game.total_difficulty * prop_neg_ach_weights))
                ** 2
            )
        if prop_pos_ach_sum < current_ach_sum:
            ach_weights = prop_pos_ach_weights
            continue
        if prop_neg_ach_sum < current_ach_sum:
            ach_weights = prop_neg_ach_weights
            continue
        exponent -= 1
    return ach_weights


def ta_weighting_loop(
    game_library: list, ta_weights: float, weight_limit: float, precision: int
) -> float:
    exponent = -1
    while exponent >= -precision:
        prop_pos_ta_weights = ta_weights + (10 ** exponent)
        prop_neg_ta_weights = ta_weights - (10 ** exponent)
        current_ta_sum = 0.0
        prop_pos_ta_sum = 0.0
        prop_neg_ta_sum = 0.0
        for game in game_library:
            game.update_ta_weights(ta_weights, weight_limit)
            current_ta_sum += game.ta_weight * (
                abs(game.ta_ratio - (game.total_difficulty * ta_weights)) ** 2
            )
            game.update_ta_weights(prop_pos_ta_weights, weight_limit)
            prop_pos_ta_sum += game.ta_weight * (
                abs(game.ta_ratio - (game.total_difficulty * prop_pos_ta_weights)) ** 2
            )
            game.update_ta_weights(prop_neg_ta_weights, weight_limit)
            prop_neg_ta_sum += game.ta_weight * (
                abs(game.ta_ratio - (game.total_difficulty * prop_neg_ta_weights)) ** 2
            )
        if prop_pos_ta_sum < current_ta_sum:
            ta_weights = prop_pos_ta_weights
            continue
        if prop_neg_ta_sum < current_ta_sum:
            ta_weights = prop_neg_ta_weights
            continue
        exponent -= 1
    return ta_weights


def gs_weighting_loop(
    game_library: list, gs_weights: float, weight_limit: float, precision: int
) -> float:
    exponent = -1
    while exponent >= -precision:
        prop_pos_gs_weights = gs_weights + (10 ** exponent)
        prop_neg_gs_weights = gs_weights - (10 ** exponent)
        current_gs_sum = 0.0
        prop_pos_gs_sum = 0.0
        prop_neg_gs_sum = 0.0
        for game in game_library:
            game.update_gs_weights(gs_weights, weight_limit)
            current_gs_sum += game.gs_weight * (
                abs(game.gs_ratio - (game.total_difficulty * gs_weights)) ** 2
            )
            game.update_gs_weights(prop_pos_gs_weights, weight_limit)
            prop_pos_gs_sum += game.gs_weight * (
                abs(game.gs_ratio - (game.total_difficulty * prop_pos_gs_weights)) ** 2
            )
            game.update_gs_weights(prop_neg_gs_weights, weight_limit)
            prop_neg_gs_sum += game.gs_weight * (
                abs(game.gs_ratio - (game.total_difficulty * prop_neg_gs_weights)) ** 2
            )
        if prop_pos_gs_sum < current_gs_sum:
            gs_weights = prop_pos_gs_weights
            continue
        if prop_neg_gs_sum < current_gs_sum:
            gs_weights = prop_neg_gs_weights
            continue
        exponent -= 1
    return gs_weights


def alpha_values(
    game_library: list, ach_weights: float, ta_weights: float, gs_weights: float
) -> tuple[float, float, float]:
    ach_alpha = 0.0
    ta_alpha = 0.0
    gs_alpha = 0.0
    alpha_diff = 0.0
    for game in game_library:
        ach_alpha = ach_alpha + game.ach_ratio
        ta_alpha = ta_alpha + game.ta_ratio
        gs_alpha = gs_alpha + game.gs_ratio
        alpha_diff = alpha_diff + game.total_difficulty

    ach_alpha = ach_alpha / len(game_library) - (
        alpha_diff / len(game_library) * ach_weights
    )
    ta_alpha = ta_alpha / len(game_library) - (
        alpha_diff / len(game_library) * ta_weights
    )
    gs_alpha = gs_alpha / len(game_library) - (
        alpha_diff / len(game_library) * gs_weights
    )
    return ach_alpha, ta_alpha, gs_alpha


def predict_gains(game_library: list, model_dict: dict) -> tuple[float, float, float]:
    total_ach_gain = 0.0
    total_ta_gain = 0.0
    total_gs_gain = 0.0
    for game in game_library:
        game.predicted_ratios(
            model_dict["ach_weights"],
            model_dict["ach_alpha"],
            model_dict["ta_weights"],
            model_dict["ta_alpha"],
            model_dict["gs_weights"],
            model_dict["gs_alpha"],
        )
        game.predicted_gains()
        if game.predicted_ach_gains > 0:
            total_ach_gain = total_ach_gain + game.predicted_ach_gains
        if game.predicted_ta_gains > 0:
            total_ta_gain = total_ta_gain + game.predicted_ta_gains
        if game.predicted_gs_gains > 0:
            total_gs_gain = total_gs_gain + game.predicted_gs_gains
    return total_ach_gain, total_ta_gain, total_gs_gain


def get_curve_fit_xy(game_library: list) -> list[list[float]]:
    xy_values = [[], [], [], []]
    for game in game_library:
        game.append_xy_value(xy_values)
    return xy_values


def predict_logistic_gains(
    game_library: list, logistic_constant: tuple[list[float], list[float], list[float]]
) -> tuple[float, float, float]:
    total_ach_gain = 0.0
    total_ta_gain = 0.0
    total_gs_gain = 0.0
    for game in game_library:
        game.predicted_logistic_ratios(logistic_constant)
        game.predicted_logistic_gains()
        # if game.predicted_logistic_ach_gains > 0:
        total_ach_gain = total_ach_gain + game.predicted_logistic_ach_gains
        # if game.predicted_logistic_ta_gains > 0:
        total_ta_gain = total_ta_gain + game.predicted_logistic_ta_gains
        # if game.predicted_logistic_gs_gains > 0:
        total_gs_gain = total_gs_gain + game.predicted_logistic_gs_gains
    return total_ach_gain, total_ta_gain, total_gs_gain
