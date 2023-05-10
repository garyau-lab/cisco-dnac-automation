import time
import yaml, json, csv
from dnacentersdk import api
from print_report import *

with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)


def pre_check():
    try:
        response = dna.sda.get_transit_peer_network_info(transit_peer_network_name=set_dict['ip_transit_name'])
        return ("exist")
    except:
        return

def post_check():
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check() == "exist":
            return ("exist")

def creation():
    payload = {
        "transitPeerNetworkName": set_dict['ip_transit_name'],
        "transitPeerNetworkType": "ip_transit",
        "ipTransitSettings": {
            "routingProtocolName": "BGP",
            "autonomousSystemNumber": str(set_dict['ip_transit_asnum'])
        },
        "sdaTransitSettings": {
            "transitControlPlaneSettings": [
                {
                    "siteNameHierarchy": "string",
                    "deviceManagementIpAddress": "string"
                }
            ]
        }
    }
    dna.sda.add_transit_peer_network(payload=payload)

print_header('Add IP Transit for SDA Fabric')
print_action(set_dict['ip_transit_name'])
if pre_check() == "exist":
    print_skip()
else:
    creation()
    if post_check() == "exist":
        print_pass()
    else:
        print_fail()
