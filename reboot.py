#!/usr/bin/python

# SCripts allows HD to reboot a meraki device that might have an issue with the tunnels or something else not coming up correctly.

#imports
import requests
import json
import os
import sys

#Private credentials file, used to make life easy when I deploy new scripts.
import cred

#custom variables for the program imported from the cred.py file located in the same directory
organization = cred.organization
key = cred.key
hub = cred.hub


#Main URL for the Meraki Platform
dashboard = "https://api.meraki.com/api/v0"
#api token and other data that needs to be uploaded in the header
headers = {'X-Cisco-Meraki-API-Key': (key), 'Content-Type': 'application/json'}

#pulls in the store number from the script that is calling this script, this is passed from the website that is calling the script.
store_input = sys.argv[1]
# need to strip off the zeros that come from the website calling the script.
store = store_input.strip("0")

#Pull the information from the Meraki cloud to get the network id
#pull back all of the networks for the organization
get_network_id_url = dashboard + '/organizations/%s/networks' % organization

#request the network data
get_network_id_response = requests.get(get_network_id_url, headers=headers)

#puts the data into json format
get_network_id_json = get_network_id_response.json()

#pull back the network_id of the store that you are configuring
for i in get_network_id_json:
    if i["name"] == str(store):
        network_id=(i["id"])

#get the device id for the network above, so that we can find the s/n of the device.
get_device_id_url = dashboard + '/networks/%s/devices' % network_id

get_device_id_response = requests.get(get_device_id_url, headers=headers)

get_device_id_json = get_device_id_response.json()

for device in get_device_id_json:
    device_id = (device["serial"])

#send the reboot command to the cloud

reboot_device_url = dashboard + '/networks/%s/devices/%s/reboot' % (network_id, device_id)
reboot_device_response = requests.post(reboot_device_url, headers=headers)
