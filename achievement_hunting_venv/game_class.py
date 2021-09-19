# Global Variables for all Games
url = "https://www.trueachievements.com"


class Game:
    """
    Create Game Class
    """

    def __init__(self, div):
        """
        Intializes the game object

        Args:
            div (str): This is the game div from html requests
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
        self.ach_ratio = self.ach_earned / self.ach_total
        self.ta_ratio = self.ta_earned / self.ta_total
        self.gs_ratio = self.gs_earned / self.gs_total
        self.total_difficulty = 1 / (self.ta_total / self.gs_total) ** 2
        self.difficulty_left = (
            1
            / ((self.ta_total - self.ta_earned) / (self.gs_total / self.gs_earned)) ** 2
        )
        self.ach_weight = 1 / max(0.001, abs(self.ach_ratio - self.total_difficulty))
        self.ta_weight = 1 / max(0.001, abs(self.ta_ratio - self.total_difficulty))
        self.gs_weight = 1 / max(0.001, abs(self.gs_ratio - self.total_difficulty))

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

    def update_ach_weights(self, weight, weight_limit):
        self.ach_weight = 1 / max(
            weight_limit, abs(self.ach_ratio - (self.total_difficulty * weight))
        )
        return self.ach_weight

    def update_ta_weights(self, weight, weight_limit):
        self.ta_weight = 1 / max(
            weight_limit, abs(self.ta_ratio - (self.total_difficulty * weight))
        )
        return self.ta_weight

    def update_gs_weights(self, weight, weight_limit):
        self.gs_weight = 1 / max(
            weight_limit, abs(self.gs_ratio - (self.total_difficulty * weight))
        )
        return self.gs_weight

    def predicted_ratios(
        self,
        total_ach_weight,
        total_ach_alpha,
        total_ta_weight,
        total_ta_alpha,
        total_gs_weight,
        total_gs_alpha,
    ):
        self.predicted_ach_ratio = min(
            1,
            ((self.total_difficulty * total_ach_weight) + total_ach_alpha)
            + (
                (1 - self.ach_ratio)
                * ((self.difficulty_left * total_ach_weight) + total_ach_alpha)
            ),
        )
        self.predicted_ta_ratio = min(
            1,
            ((self.total_difficulty * total_ta_weight) + total_ta_alpha)
            + (
                (1 - self.ta_ratio)
                * ((self.difficulty_left * total_ta_weight) + total_ta_alpha)
            ),
        )
        self.predicted_gs_ratio = min(
            1,
            ((self.total_difficulty * total_gs_weight) + total_gs_alpha)
            + (
                (1 - self.gs_ratio)
                * ((self.difficulty_left * total_gs_weight) + total_gs_alpha)
            ),
        )

    def predicted_gains(self):
        self.predicted_ach_gains = (
            self.predicted_ach_ratio * self.ach_total - self.ach_earned
        )
        self.predicted_ta_gains = (
            self.predicted_ta_ratio * self.ta_total - self.ta_earned
        )
        self.predicted_gs_gains = (
            self.predicted_gs_ratio * self.gs_total - self.gs_earned
        )
