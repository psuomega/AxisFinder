#! /usr/bin/env python3
#Author: Lucas Shaffer, 2024
#License: Do whatever you want. This code is free as in beer. 
# Originally tested/built to work using Python 3.10 on MacOS Ventura

import socket
import re
import subprocess
import platform
import json
# pip install requests if fails here
import requests
from requests.auth import HTTPDigestAuth

# Broadcast an SSDP Discovery packet and ingest responses
def locate_upnp_devices():
    webAddr = []
    textData = []
    ssdpDiscover = \
        'M-SEARCH * HTTP/1.1\r\n' \
        'HOST:239.255.255.250:1900\r\n' \
        'ST:upnp:rootdevice\r\n' \
        'MX:2\r\n' \
        'MAN:"ssdp:discover"\r\n' \
        '\r\n'
    # Set up UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # Time out value can be up to 10 for spec, but 3 is a good compromise on a fast network 
    s.settimeout(3)
    # Default Encode type is UTF-8. Send out a SSDP Discovery packet.
    s.sendto(ssdpDiscover.encode(), ('239.255.255.250', 1900) )
    # Listen for responses. Save replies for later interaction. 
    try:
        while True:
            data, addr = s.recvfrom(65507)
            webAddr.append('http://' + addr[0])
            textData.append(data.decode())
    except socket.timeout:
        pass
    s.close()
    return webAddr, textData
# Open Web Interface in Firefox, found it doesn't really play nice with Safari 
def oiff(webAddr, systype): 
    if systype == 'Darwin':
        subprocess.Popen(['open', '-a', '/Applications/Firefox.app', webAddr])
    elif systype == 'Linux':
        subprocess.Popen(['firefox', webAddr])
    elif systype == 'Windows':
        # Didn't have a Windows VM to test on.
        print ("""You can use the official Axis tool, or
               Copy Paste URL into Browser -->""", webAddr)
    else:
        print ("System Type Unrecognized or Unsupported.")

def get_dev_info (apiUrl):
    #Begin API Requests
    apiUrl = apiUrl+'/axis-cgi/'
    # Set URL for Basic Device Info API Request
    devInfo = apiUrl+'basicdeviceinfo.cgi'
    # JSON DATA for Device Info Query
    devInfoData = '{"apiVersion":"1.3","method":"getAllUnrestrictedProperties"}'
    # Post Query to Axis API
    devData = requests.post(devInfo, data=devInfoData)
    # Parse data from response
    model = devData.json()["data"]["propertyList"]["ProdNbr"]
    sn = devData.json()["data"]["propertyList"]["SerialNumber"]
    # Set URL for Firmware API Request
    fwInfo = apiUrl+'firmwaremanagement.cgi'
    # JSON DATA for Firmware API Request
    fwInfoData = '{"apiVersion":"1.4", "method":"status"}'
    # Post Data to Firmware API
    fwData = requests.post(fwInfo, auth=HTTPDigestAuth('root', 'password'), data=fwInfoData)
    if fwData.status_code == 401:
        # Assuming camera is in factory default state due to standard user/pass not working
        set_initial_user(apiUrl)
        fwData = requests.post(fwInfo, auth=HTTPDigestAuth('root', 'password'), data=fwInfoData)
    # Parse data from response  
    currVer = fwData.json()["data"]["activeFirmwareVersion"]
    # Has Firmware been updated? If it has, what is the previous version.
    if "inactiveFirmwareVersion" in fwData.json()["data"]:
        oldVer = fwData.json()["data"]["inactiveFirmwareVersion"]
    else:
        oldVer = "Firmware Is Still Factory Default"
    #Return the Model, Serial Number, Current Firmware Version, and Previous Firmware Version of the Axis Camera
    return model, sn, currVer, oldVer

def set_initial_user(apiUrl):
    setUrl = apiUrl+'pwdgrp.cgi'
    payload = {'action':'add', 'user':'root', 'pwd':'password', 'grp':'root', 'sgrp':'admin:operator:viewer:ptz'}
    r = requests.get(setUrl, params=payload)

if __name__ == '__main__':
    systype = platform.system()
    #Find the Cameras
    response = locate_upnp_devices()
    # Split returned data up into two variables. One containing the Address list, and the other containing the response from the discovery sweep
    (addrList, data) = response
    # Loop through the responses, each one that matches having -axis in the response data, open the URL in Firefox
    for each in range(len(data)):
        val = data[each]
        apiUrl = addrList[each]
        if re.search('-axis', val):
            oiff(apiUrl,systype)
            #Print off a QC Check blurb
            devInfo = get_dev_info(apiUrl)
            (model, sn, currVer, oldVer) = devInfo
            print ('\r\n\\***********************************************\\\r\n'
                'Model: %s\r\n' 
                'MAC/SN: %s\r\n' 
                'User: root\r\n' 
                'Pass: password\r\n' 
                'Firmware Status -->\r\n' 
                'Current Version: %s\r\n' 
                'Previous Version: %s\r\n\r\n'
                'Tested with Midspan POE Injector. See Documents for Proof of Operation\r\n' % (model, sn, currVer, oldVer))
