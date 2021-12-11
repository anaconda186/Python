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


def get_curve_fit_xy(game_library: list) -> list[list[float]]:
    xy_values = [[], [], [], [], []]
    process = []
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
        if game.predicted_logistic_ach_gains > 0:
            total_ach_gain = total_ach_gain + game.predicted_logistic_ach_gains
        if game.predicted_logistic_ta_gains > 0:
            total_ta_gain = total_ta_gain + game.predicted_logistic_ta_gains
        if game.predicted_logistic_gs_gains > 0:
            total_gs_gain = total_gs_gain + game.predicted_logistic_gs_gains
    return total_ach_gain, total_ta_gain, total_gs_gain


def norm_gains(game_library: list) -> None:
    max_ach_value = max(game.predicted_logistic_ach_gains for game in game_library)
    min_ach_value = min(game.predicted_logistic_ach_gains for game in game_library)
    max_ta_value = max(game.predicted_logistic_ta_gains for game in game_library)
    min_ta_value = min(game.predicted_logistic_ta_gains for game in game_library)
    max_gs_value = max(game.predicted_logistic_gs_gains for game in game_library)
    min_gs_value = min(game.predicted_logistic_ta_gains for game in game_library)

    for game in game_library:
        game.normalize_gains(
            max_ach_value,
            min_ach_value,
            max_ta_value,
            min_ta_value,
            max_gs_value,
            min_gs_value,
        )
