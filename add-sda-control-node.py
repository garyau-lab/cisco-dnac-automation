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

for i in device_dict:
    if i['fabric_role'] == "fabric-in-a-box":
        node_name = i['hostname']
        node_ip = i['ip_address']
        break


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check():
    try:
        response = dna.sda.get_control_plane_device(device_management_ip_address=node_ip)
        return ("exist")
    except:
        return

def post_check():
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check() == "exist":
            return ("exist")

def creation():
    payload = [{
        "deviceManagementIpAddress": node_ip,
        "siteNameHierarchy": site_hierarchy,
        "routeDistributionProtocol": "LISP_BGP"
    }]
    dna.sda.add_control_plane_device(payload=payload)

print_header('Add Fabric Control Plane Device')
print_action(node_name)
if pre_check() == "exist":
    print_skip()
else:
    creation()
    if post_check() == "exist":
        print_pass()
    else:
        print_fail()
