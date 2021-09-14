import requests
from bs4 import BeautifulSoup

# from openpyxl import Workbook
# from openpyxl.worksheet.table import Table, TableStyleInfo


url = "https://www.trueachievements.com"
user = "Acidreactive"
show_all = True
ach_weights = 2.0
ta_weights = 2.0
gs_weights = 2.0
weight_limit = 0.001

if show_all:
    show = "?oGamerGamesList_ShowAll=True"
else:
    show = ""


class Game:
    """
    Create Game Class
    """

    def __init__(self, div):
        """
        [summary]

        Args:
            div ([type]): [description]
        """
        self.name = div.find("td", class_="smallgame").a.text
        self.link = div.select("td:nth-of-type(2)")[0].a["href"]
        achievements = div.select("td:nth-of-type(3)")[0].text.split(" ")
        self.ach_total = int(achievements[2].replace(",", ""))
        self.ach_earned = int(achievements[0].replace(",", ""))
        ta_score = div.select("td:nth-of-type(4)")[0].text.split(" ")
        self.ta_total = int(ta_score[2].replace(",", ""))
        self.ta_earned = int(ta_score[0].replace(",", ""))
        gs_score = div.select("td:nth-of-type(5)")[0].text.split(" ")
        self.gs_total = int(
            gs_score[2].replace(",", "").replace("(", "").replace(")", "")
        )
        self.gs_earned = int(
            gs_score[0].replace(",", "").replace("(", "").replace(")", "")
        )
        self.ach_ratio = self.ach_earned/self.ach_total
        self.ta_ratio = self.ta_earned/self.ta_total
        self.gs_ratio = self.gs_earned/self.gs_total
        self.total_difficulty = 1/(self.ta_total/self.gs_total)**2
        self.difficulty_left = 1 / \
            ((self.ta_total-self.ta_earned)/(self.gs_total/self.gs_earned))**2
        self.ach_weight = 1 / \
            max(weight_limit, abs(self.ach_ratio -
                                  (self.total_difficulty*ach_weights)))
        self.ta_weight = 1 / \
            max(weight_limit, abs(self.ta_ratio -
                                  (self.total_difficulty*ta_weights)))
        self.gs_weight = 1 / \
            max(weight_limit, abs(self.gs_ratio -
                                  (self.total_difficulty*gs_weights)))

    def __str__(self):
        title = self.name
        ach = f"{self.ach_earned} of {self.ach_total} achievements"
        ta_points = f"{self.ta_earned} of {self.ta_total} TA Points"
        gs_score = f"{self.gs_earned} of {self.gs_total} GS"
        return f"\n{title}, {ach}, {ta_points}, {gs_score}, {self.ach_weight} \n{url}{self.link}"

    def __repr__(self):
        title = self.name
        ach = f"ACH Gain: {self.predicted_ach_gains}"
        ta_points = f"TA Gain: {self.predicted_ta_gains}"
        gs_score = f"GS Gain: {self.predicted_gs_gains}"
        return f"\n{title}, {ach}, {ta_points}, {gs_score}, \n{url}{self.link}"

    def update_ach_weights(self, weight):
        self.ach_weight = 1 / \
            max(weight_limit, abs(self.ach_ratio-(self.total_difficulty*weight)))
        return self.ach_weight

    def update_ta_weights(self, weight):
        self.ta_weight = 1 / \
            max(weight_limit, abs(self.ta_ratio-(self.total_difficulty*weight)))
        return self.ta_weight

    def update_gs_weights(self, weight):
        self.gs_weight = 1 / \
            max(weight_limit, abs(self.gs_ratio-(self.total_difficulty*weight)))
        return self.gs_weight

    def predicted_ratios(self):
        self.predicted_ach_ratio = min(1, ((self.total_difficulty * ach_weights) + alpha_ach) + (
            (1 - self.ach_ratio) * ((self.difficulty_left * ach_weights) + alpha_ach)))
        self.predicted_ta_ratio = min(1, ((self.total_difficulty * ta_weights) + alpha_ta) + (
            (1 - self.ta_ratio) * ((self.difficulty_left * ta_weights) + alpha_ta)))
        self.predicted_gs_ratio = min(1, ((self.total_difficulty * gs_weights) + alpha_gs) + (
            (1 - self.gs_ratio) * ((self.difficulty_left * gs_weights) + alpha_gs)))

    def predicted_gains(self):
        self.predicted_ach_gains = self.predicted_ach_ratio * \
            self.ach_total - self.ach_earned
        self.predicted_ta_gains = self.predicted_ta_ratio * \
            self.ta_total - self.ta_earned
        self.predicted_gs_gains = self.predicted_gs_ratio * \
            self.gs_total - self.gs_earned


r = requests.get(f"{url}/gamer/{user}/games{show}").text

soup = BeautifulSoup(r, "html.parser")

# for img in soup.findAll(("img"), class_=("dlcinfo")):
#     img.decompose()
# img_tag = soup.findAll("img", class_="dlcinfo")


game_library = []

for game in soup.findAll("tr", class_=("even", "odd")):
    if int(
        game.select("td:nth-of-type(5)")[0].text.split(" ")[
            2].replace(",", "").replace("(", "").replace(")", "")
    ) == 0:
        continue
    game = Game(game)

    game_library.append(game)

# Start ACH weighting Loop #
exponent = -1
while exponent >= -5:
    prop_pos_ach_weights = ach_weights + (10**exponent)
    prop_neg_ach_weights = ach_weights - (10**exponent)
    current_ach_sum = 0.0
    prop_pos_ach_sum = 0.0
    prop_neg_ach_sum = 0.0
    for game in game_library:
        game.update_ach_weights(ach_weights)
        current_ach_sum += game.ach_weight * \
            (abs(game.ach_ratio-(game.total_difficulty*ach_weights))**2)
        game.update_ach_weights(prop_pos_ach_weights)
        prop_pos_ach_sum += game.ach_weight * \
            (abs(game.ach_ratio-(game.total_difficulty*prop_pos_ach_weights))**2)
        game.update_ach_weights(prop_neg_ach_weights)
        prop_neg_ach_sum += game.ach_weight * \
            (abs(game.ach_ratio-(game.total_difficulty*prop_neg_ach_weights))**2)
    if prop_pos_ach_sum < current_ach_sum:
        ach_weights = prop_pos_ach_weights
        # print(ach_weights, exponent)
        continue
    if prop_neg_ach_sum < current_ach_sum:
        ach_weights = prop_neg_ach_weights
        # print(ach_weights, exponent)
        continue
    exponent -= 1
    # print(ach_weights, exponent)

# Start TA weighting Loop #
exponent = -1
while exponent >= -5:
    prop_pos_ta_weights = ta_weights + (10**exponent)
    prop_neg_ta_weights = ta_weights - (10**exponent)
    current_ta_sum = 0.0
    prop_pos_ta_sum = 0.0
    prop_neg_ta_sum = 0.0
    for game in game_library:
        game.update_ta_weights(ta_weights)
        current_ta_sum += game.ta_weight * \
            (abs(game.ta_ratio-(game.total_difficulty*ta_weights))**2)
        game.update_ta_weights(prop_pos_ta_weights)
        prop_pos_ta_sum += game.ta_weight * \
            (abs(game.ta_ratio-(game.total_difficulty*prop_pos_ta_weights))**2)
        game.update_ta_weights(prop_neg_ta_weights)
        prop_neg_ta_sum += game.ta_weight * \
            (abs(game.ta_ratio-(game.total_difficulty*prop_neg_ta_weights))**2)
    if prop_pos_ta_sum < current_ta_sum:
        ta_weights = prop_pos_ta_weights
        # print(ta_weights, exponent)
        continue
    if prop_neg_ta_sum < current_ta_sum:
        ta_weights = prop_neg_ta_weights
        # print(ta_weights, exponent)
        continue
    exponent -= 1
    # print(ta_weights, exponent)

# Start GS weighting Loop #
exponent = -1
while exponent >= -5:
    prop_pos_gs_weights = gs_weights + (10**exponent)
    prop_neg_gs_weights = gs_weights - (10**exponent)
    current_gs_sum = 0.0
    prop_pos_gs_sum = 0.0
    prop_neg_gs_sum = 0.0
    for game in game_library:
        game.update_gs_weights(gs_weights)
        current_gs_sum += game.gs_weight * \
            (abs(game.gs_ratio-(game.total_difficulty*gs_weights))**2)
        game.update_gs_weights(prop_pos_gs_weights)
        prop_pos_gs_sum += game.gs_weight * \
            (abs(game.gs_ratio-(game.total_difficulty*prop_pos_gs_weights))**2)
        game.update_gs_weights(prop_neg_gs_weights)
        prop_neg_gs_sum += game.gs_weight * \
            (abs(game.gs_ratio-(game.total_difficulty*prop_neg_gs_weights))**2)
    if prop_pos_gs_sum < current_gs_sum:
        gs_weights = prop_pos_gs_weights
        # print(gs_weights, exponent)
        continue
    if prop_neg_gs_sum < current_gs_sum:
        gs_weights = prop_neg_gs_weights
        # print(gs_weights, exponent)
        continue
    exponent -= 1
    # print(gs_weights, exponent)

# Alpha Values
alpha_ach = 0.0
alpha_ta = 0.0
alpha_gs = 0.0
alpha_diff = 0.0

for game in game_library:
    alpha_ach = alpha_ach + game.ach_ratio
    alpha_ta = alpha_ta + game.ta_ratio
    alpha_gs = alpha_gs + game.gs_ratio
    alpha_diff = alpha_diff + game.total_difficulty

alpha_ach = alpha_ach/len(game_library) - \
    (alpha_diff/len(game_library) * ach_weights)
alpha_ta = alpha_ta/len(game_library) - \
    (alpha_diff/len(game_library) * ta_weights)
alpha_gs = alpha_gs/len(game_library) - \
    (alpha_diff/len(game_library) * gs_weights)

# Establish predicted Values
total_ach_gain = 0.0
total_ta_gain = 0.0
total_gs_gain = 0.0
for game in game_library:
    game.predicted_ratios()
    game.predicted_gains()
    if game.predicted_ach_gains > 0:
        total_ach_gain = total_ach_gain + game.predicted_ach_gains
    if game.predicted_ta_gains > 0:
        total_ta_gain = total_ta_gain + game.predicted_ta_gains
    if game.predicted_gs_gains > 0:
        total_gs_gain = total_gs_gain + game.predicted_gs_gains


game_library.sort(key=lambda x: x.predicted_gs_gains)
# data = pd.read_excel("./achievement_hunting.xlsx")
print(game_library)
print(f"ACH: M * {ach_weights} + {alpha_ach}, TA: M * {ta_weights} + {alpha_ta}, GS: M * {gs_weights} + {alpha_gs}")
print(
    f"Total Ach gain: {total_ach_gain}, Total TA gain: {total_ta_gain}, Total GS gain: {total_gs_gain}")
