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
wireless_dict = []
with open('dnac-wireless-ap.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        wireless_dict.append(row_data)

# Read wireless profile list
profiles = []
for i in wireless_dict:
    if i['wireless_profile'] not in profiles:
        profiles.append(i['wireless_profile'])


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

def creation(profile_name,ssidDetails,floor_hierarchies):
    payload = {
        "profileDetails": {
            "name": profile_name,
            "ssidDetails": ssidDetails,
            "sites": floor_hierarchies,
        }
    }
    dna.wireless.create_wireless_profile(payload=payload)

building_hierarchies = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']
print_header('Create Wireless Profiles for Floor')
for profile in profiles:
    profile_full_name = set_dict['site_building']+" - "+profile

    # Prepare site list
    floor_names = []
    floor_hierarchies = []
    for j in wireless_dict:
        if j['wireless_profile'] == profile and j['floor_name'] not in floor_names:
           floor_names.append(j['floor_name'])
           floor_hierarchies.append(building_hierarchies+"/"+j['floor_name'])

    # Prepare SSID list
    ssidDetails = []
    ssid_names = []
    for j in wireless_dict:
        if j['wireless_profile'] == profile:
            ssid_list = j['wireless_network'].split(",")
            for ssid in ssid_list:
                ssidDetails.append({"name": ssid, "enableFabric": True})
                ssid_names.append(ssid)
            break

    # Start
    print("- Profile:  "+set_dict['site_building']+" - "+profile)
    print("  Foor:     "+str(floor_names).replace("'","").replace("[","").replace("]",""))
    print_action_l2("SSID:     "+str(ssid_names).replace("'","").replace("[","").replace("]",""))
    if pre_check(profile_full_name) == "exist":
        print_skip()
    else:
        creation(profile_full_name,ssidDetails,floor_hierarchies)
        if post_check(profile_full_name) == "exist":
            print_pass()
        else:
            print_fail()
