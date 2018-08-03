#!/usr/bin/env python
import pandas as pd
from tkinter import *
from pandastable import Table


root = Tk()
frame = Frame(root)
frame.pack(side=LEFT, expand=TRUE, fill=BOTH)

df = pd.read_csv("test All.csv")
rows, columns = df.shape
# assuming parent is the frame in which you want to place the table
pt = Table(frame, dataframe=df)
pt.show()

# Setup roster
attributes = ["Player", "Position", "Team", "Avg. Value", "Starter/Bench"]

listbox = Listbox(root)
listbox.pack(side=LEFT)

for item in list(range(rows)):
    listbox.insert(END, df["Player"].iloc[item])

redbutton = Button(root, text="Red", fg="red")
redbutton.pack(side=RIGHT)

current_team = pd.DataFrame()

root.mainloop()
