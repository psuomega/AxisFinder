#! /usr/bin/env python3
# Originally tested/built to work using Python 3.12

import socket
import re
import subprocess
import platform

ssdpDiscover = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n' \
    '\r\n'

def locate_upnp_devices():
    webAddr = []
    textData = []
    # Set up UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Time out value can be up to 10 for spec, but 2 is a good compromise on a fast network 
    s.settimeout(2)
    # Default Encode type is UTF-8. Send out a SSDP Discovery packet.
    s.sendto(ssdpDiscover.encode(), ('239.255.255.250', 1900) )

    # Listen for responses. Save replies for later interaction. 
    try:
        while True:
            data, addr = s.recvfrom(65507)
            # Default Decode type is UTF-8 
            textData.append(data.decode())
            webAddr.append('http://' + addr[0])
           
    except socket.timeout:
        pass
   
    return webAddr, textData
 

#  MacOS --> Don't want to use firefox? Change Popen to just (['open', webAddr]) to open the URL in Safari / Default Browser 

def open_in_firefox(webAddr, systype):
    
    if systype == 'Darwin':
        subprocess.Popen(['open', '-a', '/Applications/Firefox Developer Edition.app', webAddr])
    elif systype == 'Linux':
        subprocess.Popen(['firefox', webAddr])
    elif systype == 'Windows':
        # Didn't have a Windows VM to test on.
        print ("""You can use the official Axis tool, or
               Copy Paste URL into Browser -->""", webAddr)

if __name__ == '__main__':

    systype = platform.system()
    # Run ssdp discovery function, get results into response variable (webAddr, textData)
    response = locate_upnp_devices()
    # Split returned data up into two variables. One containing the Address list, and the other containing the response from the discovery sweep
    (addrList, data) = response

    # Loop through the responses, each one that matches having -axis in the response data, open the URL in Firefox
    for each in range(len(data)):
        val = data[each]
        if re.search('-axis', val):
          open_in_firefox(addrList[each], systype)

