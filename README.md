# AxisFinder
Python scripts to open web interface of Axis Camera

Axis Communications does not release a MacOS version of AXIS IP Utility, so I built this quick python script to save myself a few key strokes when I have to interface with a new camera, instead of using ```arp -a``` and parsing output to find what I want.
You can find the Official Axis IP Utility on the Axis site here: https://www.axis.com/support/tools/axis-ip-utility#download-block

How to use:
1. Plug in camera to the same network as your Mac (within broadcast range)
2. Wait for Axis camera to finish it's POST routine
3. Run Script. eg: ./Axisinterface.py

Requirements: I have the script set up to open the Axis camera page in Firefox due to issues with the Axis interface and Safari not playing nice together. Change to suit your environment.

Axisfinder.py: Opens every Axis camera's web interface it finds via SSDP Discovery in Firefox. Sets default user/pass to root:password on a factory default camera. Prints out a QC blurb.

Axisinterface.py: Searches via SSDP Discovery and displays Axis cameras found on open. Provides a button to open the Web Interface of the camera. Backend provided by Axisfinder.py. 
  Tested on Debian 13: default installation missing tkinter and requests
  ``` sudo (or su -c ') apt install python3-tk (') ```
  To install requests, create a venv ie: ``` python3 -m venv .``` in the directory you downloaded the python files to, ```source ./bin/activate``` then ```python3 -m pip install requests```

Known Issues: Firmware Version 8 doesn't provide the searched for Axis bit in the initial SSDP Discovery, but really only been using this for FW V10+
Hacks/Workaround: I changed Axisfinder to return the URLs of everything it finds in SSDP and was able to just plug through them until I found the camera I was looking for. If this is useful, let me know and I'll fork this to upload those changes. Probably even make a real fix...
