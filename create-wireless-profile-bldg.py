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

# Read SSID list
ssid_list = []
for i in ssid_dict:
    if i['ssid_name'] not in ssid_list:
        ssid_list.append(i['ssid_name'])

ssidDetails = []
ssid_names = []
for ssid in ssid_list:
    ssidDetails.append({"name": ssid,"enableFabric": True})
    ssid_names.append(ssid)

site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']
sites = [site_hierarchy]

def pre_check(profile_name):
    try:
        response = dna.wireless.get_wireless_profile(profile_name=profile_name)
        return ("exist")
    except:
        return

def post_check(profile_name):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(profile_name) == "exist":
            return ("exist")

def creation(profile_name):
    # Create Wireless Profile
    payload = {
        "profileDetails": {
            "name": profile_name,
            "ssidDetails": ssidDetails,
            "sites": sites,
        }
    }
    dna.wireless.create_wireless_profile(payload=payload)

print_header('Create Wireless Profile for Building')
print("- Profile:  "+set_dict['site_building'])
print("  Building: "+set_dict['site_building'])
print_action_l2("SSID:     "+str(ssid_names).replace("'","").replace("[","").replace("]",""))

if pre_check(set_dict['site_building']) == "exist":
    print_skip()
else:
    creation(set_dict['site_building'])
    if post_check(set_dict['site_building']) == "exist":
        print_pass()
    else:
        print_fail()
