import requests
from bs4 import BeautifulSoup

url = "https://www.trueachievements.com"
user = "Acidreactive"
show_all = True

if show_all:
    show = "?oGamerGamesList_ShowAll=True"
else:
    show = ""


class Game:
    """Creates the Game Class"""

    def __init__(self, div):
        self.name = div.find("td", class_="smallgame").a.text
        self.link = div.select("td:nth-of-type(2)")[0].a['href']
        achievements = div.select("td:nth-of-type(3)")[0].text.split(" ")
        self.achievements_total = int(achievements[2].replace(',', ''))
        self.achievements_earned = int(achievements[0].replace(',', ''))
        ta_score = div.select("td:nth-of-type(4)")[0].text.split(" ")
        self.ta_total = int(ta_score[2].replace(',', ''))
        self.ta_earned = int(ta_score[0].replace(',', ''))
        gs_score = div.select("td:nth-of-type(5)")[0].text.split(" ")
        self.gs_total = int(gs_score[2].replace(
            ',', '').replace("(", "").replace(')', ''))
        self.gs_earned = int(gs_score[0].replace(
            ',', '').replace("(", "").replace(')', ''))

    def __str__(self):
        return f"{self.name}, {self.achievements_earned} of {self.achievements_total} achievements, {self.ta_earned} of {self.ta_total} TA Points, {self.gs_earned} of {self.gs_total} GS, {url}{self.link}"


r = requests.get(f"{url}/gamer/{user}/games{show}").text

soup = BeautifulSoup(r, "html.parser")

# for img in soup.findAll(("img"), class_=("dlcinfo")):
#     img.decompose()
# img_tag = soup.findAll("img", class_="dlcinfo")


game_library = []

for game in soup.findAll("tr", class_=("even", "odd")):
    game_library.append(Game(game))

for game in game_library:
    print(game)
