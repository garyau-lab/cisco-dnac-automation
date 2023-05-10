import time
import yaml, json, csv
from dnacentersdk import api
from print_report import *


with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)
    
dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)

# Read site-id 
site_id = dna.sites.get_site(name=set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building'])['response'][0]['id']

# Read subpools from CSV file as an array of dictionary
subpools_dict = []
with open('dnac-subpool.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        subpools_dict.append(row_data)


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check(subpool):
    responses = dna.network_settings.get_reserve_ip_subpool(site_id=site_id)['response']
    subnet = subpool['subnet'] + "/" + subpool['mask']
    for response in responses:
        ipools = response['ipPools'][0]
        if ipools['ipPoolName'] == subpool['pool_name'] and ipools['ipPoolCidr'] == subnet:
            return ("exist")
    return

def post_check(subpool):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(subpool) == "exist":
            return ("exist")

def creation(subpool):
    payload = {
        "name": subpool['pool_name'],
        "type": "LAN",
        "ipv4GlobalPool": subpool['global_pool_net'],
        "ipv4Subnet": subpool['subnet'],
        "ipv4PrefixLength": int(subpool['mask']),
        "ipv4GateWay": subpool['gateway'],
        "ipv4DhcpServers": [
            subpool['dhcp_server']
        ],
        "ipv4DnsServers": [
            subpool['dns_server']
        ],
    }
    dna.network_settings.reserve_ip_subpool(site_id=site_id, payload=payload)

print_header('Create Subpool')
for subpool in subpools_dict:
    print_action(subpool['pool_name'] + " " + subpool['subnet'] + "/" + subpool['mask'])
    if pre_check(subpool) == "exist":
        print_skip()
    else:
        creation(subpool)
        if post_check(subpool) == "exist":
            print_pass()
        else:
            print_fail()

