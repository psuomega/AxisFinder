#!/bin/bash

#V1.01 Update -Changed Open from default browser to specify Firefox to avoid Safari issues
#V1.00 Initial Version - Search ARP table for a newly connected Axis camera on the same switch.
#Author: Lucas Shaffer, 2020-2023
#License: Do whatever you want. This code is free as in beer. 

result=""
url=""
# Check ARP table for Axis Entries. Grab the first 23 characters of the first entry (axis-$$MAC.local).
result=$(arp -a | grep axis)
url="http://${result:0:23}"
# Open .local address in Firefox because the Axis camera's site doesn't play nice with Safari.
open -a /Applications/Firefox\ Developer\ Edition.app/ $url
