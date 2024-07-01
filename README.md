# AxisFinder
Bash and Python scripts to open web interface of Axis Camera

Axis Communications does not release a MacOS version of AXIS IP Utility, so I built this quick shell script to save myself a few key strokes when I have to interface with a new camera. 
You can find the Windows version on the Axis site here: https://www.axis.com/support/tools/axis-ip-utility#download-block

How to use:
1. Plug in camera to the same switch as your Mac (if using shell script)
2. Wait for Axis camera to finish it's POST routine
3. Run Script. eg: ./AxisFinder.sh or ./AxisFinder.py

Requirements: I have the script set up to open the Axis camera page in Firefox due to issues with the Axis interface and Safari not playing nice together. Change to suit your environment.

Shell Script Limitations: Since it relies on an ARP table query, you must be close enough to receive the layer 2 packets. I designed it to work with MacOS, but since it's using bash, may also work for Linux with a few simple modifications.

Python Script: Opens every Axis camera's web interface it finds via SSDP Discovery in Firefox. Sets default user/pass to root:password on a factory default camera. Prints out a QC blurb.

GUI only Alternatives: Discovery by Lily Ballard ( https://apps.apple.com/us/app/discovery-dns-sd-browser/id1381004916?mt=12 )
Lily's program works with Bonjour (DNS-SD) and will let you find cameras further away. Look for _axis entries.
