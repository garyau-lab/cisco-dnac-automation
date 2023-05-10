import time
import yaml, json, csv
from dnacentersdk import api
from print_report import *

with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)


# Read CSV file as an array of dictionary
subpools_dict = []
with open('dnac-subpool.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        subpools_dict.append(row_data)


# Read the required subpools
subpools = []
for i in subpools_dict:
    if i['vn_name'] != "":
        subpools.append(i)


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check(subpool):
    response = dna.sda.get_ip_pool_from_sda_virtual_network(site_name_hierarchy=site_hierarchy, virtual_network_name=subpool['vn_name'], ip_pool_name=subpool['pool_name'])
    if response['status'] == "success":
        return ("exist")
    else:
        return

def post_check(subpool):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(subpool) == "exist":
            return ("exist")

def creation(subpool):
    payload = {
        "siteNameHierarchy": site_hierarchy,
        "virtualNetworkName": subpool['vn_name'],
        "ipPoolName": subpool['pool_name'],
        "vlanName": subpool['pool_name'],
        "autoGenerateVlanName": False,
        "trafficType": subpool['traffic_type'],
        "scalableGroupName": subpool['sgt_name'],
        "isWirelessPool": True,
    }
    if subpool['vn_name'] == "INFRA_VN":
        payload["poolType"] ="AP"
    dna.sda.add_ip_pool_in_sda_virtual_network(payload=payload)

print_header('Add Subpool to Virtual Network')
for subpool in subpools:
    print_action(subpool['vn_name']+" "+subpool['pool_name'])
    if pre_check(subpool) == "exist":
        print_skip()

    else:
        creation(subpool)
        if post_check(subpool) == "exist":
            print_pass()
        else:
            print_fail()
        
