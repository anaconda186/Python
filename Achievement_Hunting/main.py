import requests
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
        self.link = div.select("td:nth-of-type(2)")[0].a['href']
        achievements = div.select("td:nth-of-type(3)")[0].text.split(" ")
        self.ach_total = int(achievements[2].replace(',', ''))
        self.ach_earned = int(achievements[0].replace(',', ''))
        ta_score = div.select("td:nth-of-type(4)")[0].text.split(" ")
        self.ta_total = int(ta_score[2].replace(',', ''))
        self.ta_earned = int(ta_score[0].replace(',', ''))
        gs_score = div.select("td:nth-of-type(5)")[0].text.split(" ")
        self.gs_total = int(gs_score[2].replace(
            ',', '').replace("(", "").replace(')', ''))
        self.gs_earned = int(gs_score[0].replace(
            ',', '').replace("(", "").replace(')', ''))

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
ws1.title = "Game Data"
header1 = ["Title", "Achievements Earned", "Achievements Total",
           "TA Earned", "TA Total", "GS Earned", "GS Total"]
ws1.append(header1)
# ws1['A1'] = "Title"
# ws1['B1'] = "Achievements Earned"
# ws1['C1'] = "Achievements Total"
# ws1['D1'] = "TA Earned"
# ws1['E1'] = "TA Total"
# ws1['F1'] = "GS Earned"
# ws1['G1'] = "GS Total"
ws2 = wb.create_sheet(title="Meta Data")
header2 = ["Title", "ACH Ratio", "TA Ratio", "GS Ratio"]
ws2.append(header2)
# ws2['A1'] = "Title"
# ws2['B1'] = "ACH Ratio"
# ws2['C1'] = "TA Ratio"
# ws2['D1'] = "GS Ratio"

row = 1
game_library = []

for game in soup.findAll("tr", class_=("even", "odd")):

    new_game = Game(game)
    if int(new_game.gs_total) == 0:
        continue
    game_library.append(new_game)
    row += 1
    data1 = [new_game.name, new_game.ach_earned, new_game.ach_total,
             new_game.ta_earned, new_game.ta_total, new_game.gs_earned, new_game.gs_total]
    ws1.append(data1)
    ws1[f"A{row}"].hyperlink = url+new_game.link
    ws1[f"A{row}"].style = "Hyperlink"
    # ws1[f"A{row}"].value = new_game.name
    # ws1[f"B{row}"] = new_game.ach_earned
    # ws1[f"C{row}"] = new_game.ach_total
    # ws1[f"D{row}"] = new_game.ta_earned
    # ws1[f"E{row}"] = new_game.ta_total
    # ws1[f"F{row}"] = new_game.gs_earned
    # ws1[f"G{row}"] = new_game.gs_total
    data2 = [f"='Game Data'!A{row}", f"='Game Data'!B{row}/'Game Data'!C{row}",
             f"='Game Data'!D{row}/'Game Data'!E{row}", f"='Game Data'!F{row}/'Game Data'!G{row}"]
    ws2.append(data2)
    # ws2[f"A{row}"] = new_game.name
    # ws2[f"B{row}"] = f"='Game Data'!B{row}/'Game Data'!C{row}"
    # ws2[f"C{row}"] = f"='Game Data'!D{row}/'Game Data'!E{row}"
    # ws2[f"D{row}"] = f"='Game Data'!F{row}/'Game Data'!G{row}"
    print(new_game)

tab = Table(displayName="Game_List", ref=f"A1:g{row}")

# Add a default style with striped rows and banded columns
style = TableStyleInfo(name="TableStyleMedium7",
                       showFirstColumn=True, showRowStripes=True)
tab.tableStyleInfo = style


ws1.add_table(tab)
wb.save("./Achievement_Hunting/achievement_hunting.xlsx")
