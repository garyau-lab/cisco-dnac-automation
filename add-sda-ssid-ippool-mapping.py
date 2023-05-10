import time, warnings
import yaml, json, csv
from dnacentersdk import api
from print_report import *

warnings.filterwarnings("ignore")

with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)

# Read CSV file as an array of dictionary
ssid_dict = []
with open('dnac-wireless-ssid.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        ssid_dict.append(row_data)


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check(ssid):
    try:
        response = dna.fabric_wireless.get_ssid_to_ip_pool_mapping(site_name_hierarchy=site_hierarchy, vlan_name=ssid['pool_name'])
        if response['ssidDetails'] != []:
            return ("exist")
    except:
        return

def post_check(ssid):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(ssid) == "exist":
            return ("exist")

def creation(ssid):
    payload = {
        "vlanName": ssid['pool_name'],
        "scalableGroupName": ssid['sgt_name'],
        "ssidNames": [
            ssid['ssid_name']
        ],
        "siteNameHierarchy": site_hierarchy
    }
    dna.fabric_wireless.add_ssid_to_ip_pool_mapping(payload=payload)

print_header('Add Fabric SSID to IP Pool Mapping')
for ssid in ssid_dict:
    print_action(ssid['ssid_name']+" ["+ssid['pool_name']+", "+ssid['sgt_name']+"]")
    if pre_check(ssid) == "exist":
        print_skip()
    else:
        creation(ssid)
        if post_check(ssid) == "exist":
            print_pass()
        else:
            print_fail()
