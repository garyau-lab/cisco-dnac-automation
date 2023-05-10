import time
import yaml, json, csv
from dnacentersdk import api
from print_report import *

with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)

# Read subpools from CSV file as an array of dictionary
subpools_dict = []
with open('dnac-subpool.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        subpools_dict.append(row_data)

global_pools = []
for i in subpools_dict:
    global_pool = {}
    global_pool['global_pool_name'] = i['global_pool_name']
    global_pool['global_pool_net'] = i['global_pool_net']
    if global_pool not in global_pools:
        global_pools.append(global_pool)


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check(dna_pool):
    dna_pools = dna.network_settings.get_global_pool()['response']
    for dna_pool in dna_pools:
        if dna_pool['ipPoolName'] == pool['global_pool_name'] and dna_pool['ipPoolCidr'] == pool['global_pool_net']:
            return ("exist")
    return

def post_check(pool):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(pool) == "exist":
            return ("exist")

def creation(pool):
    payload = {
        "settings": {
            "ippool": [
                {
                    "ipPoolName": pool['global_pool_name'],
                    "type": "Generic",
                    "ipPoolCidr": pool['global_pool_net'],
                    "IpAddressSpace": "IPv4",
                }
            ]
        }
    }
    dna.network_settings.create_global_pool(payload=payload)

print_header('Create Global Pool')
for pool in global_pools:
    print_action(pool['global_pool_name']+ " " + pool['global_pool_net'])
    if pre_check(pool) == "exist":
        print_skip()
    else:
        creation(pool)
        if post_check(pool) == "exist":
            print_pass()
        else:
            print_fail()
