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

# Read VN list
vn_list = []
for i in subpools_dict:
    if i['vn_name'] not in vn_list and i['vn_name'] != "":
        vn_list.append(i['vn_name'])


def pre_check(vn_name):
    try:
        response = dna.sda.get_virtual_network_with_scalable_groups(virtual_network_name=vn_name)
        return ("exist")
    except:
        return

def post_check(vn_name):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(vn_name) == "exist":
            return ("exist")

def creation(vn_name):
    payload = {
        "virtualNetworkName": vn_name,
    }    
    dna.sda.add_virtual_network_with_scalable_groups(payload=payload)

print_header('Create Virtual Network')
for vn in vn_list:
    print_action(vn)
    if pre_check(vn) == "exist":
        print_skip()

    else:
        creation(vn)
        if post_check(vn) == "exist":
            print_pass()
        else:
            print_fail()
         
