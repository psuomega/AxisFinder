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
Label(mainframe, text="Axis Model").grid(column=1, row=1, sticky=W)
Label(mainframe, text="IP Address").grid(column=2, row=1, sticky=W)
Label(mainframe, text="Serial No").grid(column=3, row=1, sticky=W)
Label(mainframe, text="FW Version").grid(column=4, row=1, sticky=W)
Label(mainframe, text="Open in Browser").grid(column=5, row=1, sticky=W)

# Perform SSDP Discovery and populate Rows.
response = Axisfinder.locate_upnp_devices()
(addrList, data) = response
i = 2
for each in range(len(data)):
        val = data[each]
        apiUrl = addrList[each]
        if re.search('-axis', val):
            devInfo = Axisfinder.get_dev_info(apiUrl)
            (model, sn, currVer, oldVer) = devInfo
            Label(mainframe, text=model).grid(column=1, row=i, sticky=W)
            Label(mainframe, text=apiUrl).grid(column=2, row=i, sticky=W)
            Label(mainframe, text=sn).grid(column=3, row=i, sticky=W)
            Label(mainframe, text=currVer).grid(column=4, row=i, sticky=W)
            btn = Button(mainframe, text="Browser", command=lambda: Axisfinder.oiff(apiUrl,systype)).grid(column=5, row=i, sticky=W)
            i += i
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
root.mainloop()
