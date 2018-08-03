#!/usr/bin/env python

import pandas as pd
import win32com.client as win32
import os


def get_auction_values(position_main="All"):

    df = pd.DataFrame()
    i = 1
    position_str = ""
    # Limit search results to 200 results
    limit = 200

    if position_main != "All":
        position_str = "&position=" + position_main
        # Limit individual position searches to 100 results
        limit = 100

    while i < limit:
        url = "http://fantasy.nfl.com/draftcenter/breakdown?offset=" + str(i) + "&sort=draftAverageAuctionCost" + position_str
        # Returns as 1x1 LIST of DataFrame objects
        table = pd.read_html(url, flavor="html5lib")
        # Extract the first element of the 1x1 list
        df = df.append(table[0])
        # NFL.com pages are limited to 25 results per page
        i += 25

    # Remove unnecessary top level row
    df.columns = df.columns.droplevel(0)
    df = df.reset_index()
    rows, cols = df.shape

    # Initialize empty columns for Positions and Teams
    new_col = [''] * rows
    # Index list from 1 to 100 or 1 to 200 depending on query
    index_list = list(range(rows))
    # Add new column for Position
    df.insert(1, "Position", new_col)
    # Add new column for Team
    df.insert(2, "Team", new_col)

    # iterate through all player cells and populate player name, position, and team by parsing out current information
    for index in index_list:
        player = df["Player"].iloc[index]

        # remove "View News" or "View Videos" from player name
        player = player.replace(" View Videos", "").replace(" View News", "").replace(" NWT", "")

        try:
            if not player[-3:] == "DEF":
                # For all individual players
                player_position, team = player.split(' - ', 1)
                second_space_index = len(player_position) - player_position[::-1].find(" ") - 1
                player = player_position[:second_space_index]
                position = player_position[second_space_index+1:]

            else:
                # For all Defenses
                player = player[:-4]
                team = player
                position = "DEF"

        except ValueError:
            # For current players NOT on a team
            second_space_index = len(player) - player[::-1].find(" ") - 1
            position = player[second_space_index+1:1]
            player = player[:second_space_index]
            team = "N/A"

        df["Player"].iloc[index] = player
        df["Position"].iloc[index] = position
        df["Team"].iloc[index] = team

    df = df.drop(columns=['index', 'Avg. Pick (ADP)', 'Avg. Round'])

    df.to_csv("test %s.csv" % position_main)
    excel_filename = "2018 NFL FF Auction Values Spreadsheet %s.xlsx" % position_main
    writer = pd.ExcelWriter(excel_filename)
    df.to_excel(writer, 'Sheet1')
    worksheet = writer.sheets['Sheet1']
    worksheet.autofilter('A1:E1')
    writer.save()
    writer.close()

    excel = win32.gencache.EnsureDispatch('Excel.Application')
    dir_current = os.getcwd()
    wb = excel.Workbooks.Open(dir_current + "\\" + excel_filename)
    ws = wb.Worksheets("Sheet1")

    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()

    return df


if __name__ == "__main__":
    get_auction_values()
