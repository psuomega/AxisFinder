#! /usr/bin/env python3
#Author: Lucas Shaffer, 2024
#License: Do whatever you want. This code is free as in beer. 

from tkinter import *
from tkinter import ttk
import Axisfinder
import platform
import re

# Get the platform type so we know where the browser lives
systype = platform.system()
# Set up our Main Winodw
root = Tk()
root.title("Axis Camera Utility")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Create first row with Column Labels
Label(mainframe, text="Axis Model", font=("Arial", 16)).grid(column=1, row=1, sticky=W)
Label(mainframe, text="IP Address", font=("Arial", 16)).grid(column=2, row=1, sticky=W)
Label(mainframe, text="Serial No", font=("Arial", 16)).grid(column=3, row=1, sticky=W)
Label(mainframe, text="FW Version", font=("Arial", 16)).grid(column=4, row=1, sticky=W)
Label(mainframe, text="Web Interface", font=("Arial", 16)).grid(column=5, row=1, sticky=W)


# Set up Button Function to open browser
def button_pressed(row):
    Axisfinder.oiff(dictUrl[row], systype)

# Perform SSDP Discovery and populate Rows.
response = Axisfinder.locate_upnp_devices()
(addrList, data) = response
i = 2
dictUrl = {}
btns = {}
for each in range(len(data)):
        val = data[each]
        if re.search('-axis', val):
            dictUrl[i] = addrList[each]
            devInfo = Axisfinder.get_dev_info(dictUrl[i])
            (model, sn, currVer, oldVer) = devInfo
            Label(mainframe, text=model, font=("Arial", 14)).grid(column=1, row=i, sticky=W)
            Label(mainframe, text=dictUrl[i], font=("Arial", 14)).grid(column=2, row=i, sticky=W)
            Label(mainframe, text=sn, font=("Arial", 14)).grid(column=3, row=i, sticky=W)
            Label(mainframe, text=currVer, font=("Arial", 14)).grid(column=4, row=i, sticky=W)
            btns[i] = Button(mainframe, text="Open", command=lambda row = i: button_pressed(row)).grid(column=5, row=i, sticky=E)
            i += i
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
