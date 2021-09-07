wb = Workbook(write_only=False)
ws1 = wb.active
ws1.title = "Game"
header1 = [
    "Title",
    "Achievements Earned",
    "Achievements Total",
    "TA Earned",
    "TA Total",
    "GS Earned",
    "GS Total",
]
ws1.append(header1)
ws2 = wb.create_sheet(title="Meta Data")
header2 = ["Title", "ACH Ratio", "TA Ratio",
           "GS Ratio", "TA-Ratio", "Total Diff", "Diff Left"]
ws2.append(header2)
row = 1

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
    game.ach_ratio,
    game.ta_ratio,
    game.gs_ratio,
    f"='Game'!E{row}/'Game'!G{row}",
    game.total_difficulty,
    game.difficulty_left
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
