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

# Read VN column
vn_list = []
for subpool in subpools_dict:
    vn_list.append(subpool['vn_name'])

# Remove empty string
vn_list = list(filter(None, vn_list))

# Remove duplicated VN
vn_list = list(dict.fromkeys(vn_list))


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check(vn_name):
    try:
        response = dna.sda.get_vn(virtual_network_name=vn_name, site_name_hierarchy=site_hierarchy)
        return ("exist")
    except:
        return

def post_check(vn_name):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(vn_name) == "exist":
            return ("exist")

def creation(vn_name):
    # Special remark: Documentation states payload is a dictionary, but SDK asks for a list.
    payload = [
        {
        "virtualNetworkName": vn_name,
        "siteNameHierarchy": site_hierarchy
        }
    ]
    dna.sda.add_vn(payload=payload)

print_header('Add Virtual Network to Fabric Site')
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
       



