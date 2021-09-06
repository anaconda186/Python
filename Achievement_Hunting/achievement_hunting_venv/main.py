import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo


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

    def __str__(self):
        title = self.name
        ach = f"{self.ach_earned} of {self.ach_total} achievements"
        ta_points = f"{self.ta_earned} of {self.ta_total} TA Points"
        gs_score = f"{self.gs_earned} of {self.gs_total} GS"
        return f"{title}, {ach}, {ta_points}, {gs_score}, {url}{self.link}"


r = requests.get(f"{url}/gamer/{user}/games{show}").text

soup = BeautifulSoup(r, "html.parser")

# for img in soup.findAll(("img"), class_=("dlcinfo")):
#     img.decompose()
# img_tag = soup.findAll("img", class_="dlcinfo")

wb = Workbook(write_only=False)
ws1 = wb.active
ws1.title = "Game"
header1 = [
    "Title",
    "Achievements Earned",
    "Achievements Total",
    "TS Earned",
    "TS Total",
    "GS Earned",
    "GS Total",
]
ws1.append(header1)
ws2 = wb.create_sheet(title="Meta Data")
header2 = ["Title", "ACH Ratio", "TS Ratio", "GS Ratio", "TA-Ratio"]
ws2.append(header2)
row = 1
game_library = []

for game in soup.findAll("tr", class_=("even", "odd")):

    game = Game(game)
    if int(game.gs_total) == 0:
        continue
    game_library.append(game)
    row += 1
    data1 = [
        game.name,
        game.ach_earned,
        game.ach_total,
        game.ta_earned,
        game.ta_total,
        game.gs_earned,
        game.gs_total,
    ]
    ws1.append(data1)
    ws1[f"A{row}"].hyperlink = url + game.link
    ws1[f"A{row}"].style = "Hyperlink"
    data2 = [
        f"='Game'!A{row}",
        f"='Game'!B{row}/'Game'!C{row}",
        f"='Game'!D{row}/'Game'!E{row}",
        f"='Game'!F{row}/'Game'!G{row}",
        f"='Game'!E{row}/'Game'!G{row}",
    ]
    ws2.append(data2)
    # print(game)

tab = Table(displayName="Game_List", ref=f"A1:g{row}")

# Add a default style with striped rows and banded columns
style = TableStyleInfo(
    name="TableStyleMedium7", showFirstColumn=True, showRowStripes=True
)
tab.tableStyleInfo = style

ws1.add_table(tab)
wb.save("./achievement_hunting.xlsx")

data = pd.read_excel("./achievement_hunting.xlsx")
print(data)
