url = "https://www.trueachievements.com"


class Game:
    """
    Create Game Class
    """

    __slots__ = [
        "name",
        "link",
        "ach_total",
        "ach_earned",
        "ta_total",
        "ta_earned",
        "gs_total",
        "gs_earned",
        "ach_ratio",
        "ta_ration",
        "ta_ratio",
        "gs_ratio",
        "total_difficulty",
        "difficulty_left",
        "predicted_logistic_ach_gains",
        "predicted_logistic_ach_ratio",
        "predicted_logistic_gs_gains",
        "predicted_logistic_gs_ratio",
        "predicted_logistic_ta_gains",
        "predicted_logistic_ta_ratio",
        "norm_logistic_ach_gains",
        "norm_logistic_gs_gains",
        "norm_logistic_ta_gains",
        "total_norm_value",
    ]

    def __init__(self, div) -> None:
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
        if self.gs_total == self.gs_earned:
            self.difficulty_left = 1
        else:
            self.difficulty_left = (
                1
                / ((self.ta_total - self.ta_earned) / (self.gs_total / self.gs_earned))
                ** 2
            )

    def __str__(self) -> str:
        title = self.name
        ach = f"{self.ach_earned} of {self.ach_total} achievements"
        ta_points = f"{self.ta_earned} of {self.ta_total} TA Points"
        gs_score = f"{self.gs_earned} of {self.gs_total} GS"
        return f"\n{title} | {ach} | {ta_points} | {gs_score} | {self.total_difficulty}\nAchievement gain: {self.predicted_logistic_ach_gains:.0f} | TrueAchievement gain: {self.predicted_logistic_ta_gains:.0f} | Gamerscore gain: {self.predicted_logistic_gs_gains:.0f}\n{url}{self.link}"

    def __repr__(self) -> str:
        title = self.name
        ach = f"{self.ach_earned} of {self.ach_total} achievements"
        ta_points = f"{self.ta_earned} of {self.ta_total} TA Points"
        gs_score = f"{self.gs_earned} of {self.gs_total} GS"
        return f"\n\n{title} | {ach} | {ta_points} | {gs_score} | {self.total_difficulty}\nAchievement gain: {self.norm_logistic_ach_gains:.2f} ({self.predicted_logistic_ach_gains:.0f}) | TrueAchievement gain: {self.norm_logistic_ta_gains:.2f} ({self.predicted_logistic_ta_gains:.0f}) | Gamerscore gain: {self.norm_logistic_gs_gains:.2f} ({self.predicted_logistic_gs_gains:.0f})\n{url}{self.link}"

    def append_xy_value(
        self,
        list_of_list: tuple[
            list[float], list[float], list[float], list[float], list[float]
        ],
    ) -> None:
        list_of_list[0].append(self.total_difficulty)
        list_of_list[1].append(self.difficulty_left)
        list_of_list[2].append(self.ach_ratio)
        list_of_list[3].append(self.ta_ratio)
        list_of_list[4].append(self.gs_ratio)

    def predicted_logistic_ratios(
        self, logistic_constant: tuple[list[float], list[float], list[float]]
    ) -> None:
        self.predicted_logistic_ach_ratio = logistic_constant[0][3] + (
            (logistic_constant[0][0] - logistic_constant[0][3])
            / (
                (
                    1
                    + (
                        (self.total_difficulty / logistic_constant[0][2])
                        ** logistic_constant[0][1]
                    )
                )
                ** logistic_constant[0][4]
            )
        )
        self.predicted_logistic_ta_ratio = logistic_constant[1][3] + (
            (logistic_constant[1][0] - logistic_constant[1][3])
            / (
                (
                    1
                    + (
                        (self.total_difficulty / logistic_constant[1][2])
                        ** logistic_constant[1][1]
                    )
                )
                ** logistic_constant[1][4]
            )
        )
        self.predicted_logistic_gs_ratio = logistic_constant[2][3] + (
            (logistic_constant[2][0] - logistic_constant[2][3])
            / (
                (
                    1
                    + (
                        (self.total_difficulty / logistic_constant[2][2])
                        ** logistic_constant[2][1]
                    )
                )
                ** logistic_constant[2][4]
            )
        )

    def predicted_logistic_gains(self) -> None:
        self.predicted_logistic_ach_gains = (
            self.predicted_logistic_ach_ratio * self.ach_total - self.ach_earned
        )
        self.predicted_logistic_ta_gains = (
            self.predicted_logistic_ta_ratio * self.ta_total - self.ta_earned
        )
        self.predicted_logistic_gs_gains = (
            self.predicted_logistic_gs_ratio * self.gs_total - self.gs_earned
        )

    def normalize_gains(
        self,
        max_ach_value,
        min_ach_value,
        max_ta_value,
        min_ta_value,
        max_gs_value,
        min_gs_value,
    ) -> None:
        self.norm_logistic_ach_gains = (
            self.predicted_logistic_ach_gains - min_ach_value
        ) / (max_ach_value - min_ach_value)
        self.norm_logistic_ta_gains = (
            self.predicted_logistic_ta_gains - min_ta_value
        ) / (max_ta_value - min_ta_value)
        self.norm_logistic_gs_gains = (
            self.predicted_logistic_gs_gains - min_gs_value
        ) / (max_gs_value - min_gs_value)
        self.total_norm_value = (
            self.norm_logistic_ach_gains
            + self.norm_logistic_ta_gains
            + self.norm_logistic_gs_gains
        )
