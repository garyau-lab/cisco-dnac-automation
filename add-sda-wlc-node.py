import time
import yaml, json, csv
from dnacentersdk import api
from print_report import *

with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)

# Read CSV file as an array of dictionary
device_dict = []
with open('dnac-device.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        device_dict.append(row_data)

subnet_dict = []
with open('dnac-subpool.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        subnet_dict.append(row_data)

fabric_dict = []
with open('dnac-l3handoff.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        fabric_dict.append(row_data)

for i in device_dict:
    if i['fabric_role'] == "fabric-in-a-box":
        node_name = i['hostname']
        node_ip = i['ip_address']
        break

for i in subnet_dict:
    if i['pool_type'] == "transit":
        transit_pool = i['pool_name']
        break


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']
print (site_hierarchy)

payload = {
    "deviceName": "LON-BDR-SW-01.test.local",
    "siteNameHierarchy": "Global/EMEAR/UK/London/London SDA"
}
response = dna.fabric_wireless.add_w_l_c_to_fabric_domain(deviceName="LON-BDR-SW-01.test.local", siteNameHierarchy=site_hierarchy)
print (json.dumps(response, indent=2))


#def pre_check():
#    try:
#        response = dna.sda.gets_border_device_detail(device_management_ip_address=node_ip)
#        return ("exist")
#    except:
#        return
#
#def post_check():
#    for i in range(set_dict['verify_retry_normal']):
#        time.sleep(set_dict['verify_delay'])
#        if pre_check() == "exist":
#            return ("exist")
#
#def creation():
#    payload = [
#        {
#            "deviceManagementIpAddress": node_ip,
#            "siteNameHierarchy": site_hierarchy,
#            "deviceRole": [
#                "Control_Plane_Node",
#                "Border_Node",
#                "Edge_Node"
#            ],
#            "routeDistributionProtocol": "LISP_BGP",
#            "externalDomainRoutingProtocolName": "BGP",
#            "externalConnectivityIpPoolName": transit_pool,
#            "internalAutonomouSystemNumber": str(set_dict['local_asnum']),
#            "borderSessionType": "EXTERNAL",
#            "connectedToInternet": "true",
#            "borderWithExternalConnectivity": "true",
#            "externalConnectivitySettings": [
#                {   
#                    "interfaceName": set_dict['external_interface'],
#                    "interfaceDescription": "",
#                    "externalAutonomouSystemNumber": str(set_dict['ip_transit_asnum']),
#                    "l3Handoff": l3Handoffs_pl
#                }
#            ]
#        }
#    ]
#    dna.sda.adds_border_device(payload=payload)
#
#def contruct_l3Handoff_payload():
#    l3Handoffs = []
#    for i in fabric_dict:
#        l3Handoff_vn = {}
#        l3Handoff_vn['virtualNetworkName'] = i['vn_name']
#        l3Handoff_vn['vlanId'] = i['vlan_id']
#
#        l3Handoff = {}
#        l3Handoff['virtualNetwork'] = l3Handoff_vn
#        l3Handoffs.append(l3Handoff)
#    return (l3Handoffs)
#
#print_header('Add Fabric-in-a-Box Node')
#print_action(node_name)
#l3Handoffs_pl = contruct_l3Handoff_payload()
#if pre_check() == "exist":
#    print_skip()
#else:
#    creation()
#    if post_check() == "exist":
#        print_pass()
#    else:
#        print_fail()
#