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


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']
site_id = dna.sites.get_site(name=site_hierarchy)['response'][0]['id']

def pre_check(device):
    hostname1 = device['hostname'].split(".")[0]
    try:
        device_list = dna.devices.devices(site_id=site_id)['response']
        for i in device_list:
            hostname2 = i['name'].split(".")[0]
            if hostname1 == hostname2:
                return ("exist")
    except:
        return

def post_check(device):
    for i in range(set_dict['verify_retry_extended']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(device) == "exist":
            return ("exist")

def creation(device):
    payload = {
        "device": [
            {
                "ip": device['ip_address']
            }
        ]
    }
    dna.sites.assign_devices_to_site(site_id=site_id, payload=payload)

creation_list = []
print_header('Assign Unassigned-Device to Site')
for device in device_dict:
    if pre_check(device) == "exist":
        print_action(device['hostname'])
        print_skip()
    else:
        creation(device)
        creation_list.append(device['hostname'])

for i in creation_list:
    for device in device_dict:
        if device['hostname'] == i:
            print_action(device['hostname'])
            if post_check(device) == "exist":
                print_pass()
            else:
                print_fail()