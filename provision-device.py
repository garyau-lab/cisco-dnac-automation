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

def pre_check(device):
    try:
        dna.sda.get_provisioned_wired_device(device_management_ip_address=device['ip_address'])
        return ("exist")
    except:
        return

def post_check(device):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(device) == "exist":
            return ("exist")

def creation(device):
    dna.sda.provision_wired_device(deviceManagementIpAddress=device['ip_address'], siteNameHierarchy=site_hierarchy)

print_header('Provision Device')
for device in device_dict:
    print_action(device['hostname'])
    if pre_check(device) == "exist":
        print_skip()
    else:
        creation(device)
        if post_check(device) == "exist":
            print_pass()
        else:
            print_fail()
