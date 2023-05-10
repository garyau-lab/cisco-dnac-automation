import time
import yaml, json, csv
from dnacentersdk import api
from print_report import *

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

# Read floor list
floors = []
for i in wireless_dict:
    if i['floor_name'] not in floors:
        floors.append(i['floor_name'])


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check(floor_name):
    try:
        response = dna.sites.get_site(name=site_hierarchy+"/"+floor_name)
        return ("exist")
    except:
        return

def post_check(floor_name):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check(floor_name) == "exist":
            return ("exist")

def creation(floor_name):
    # Create Floor
    payload = {
        "type": "floor",
        "site": {
            "floor": {
                "name": floor_name,
                "parentName": site_hierarchy,
                "rfModel": "Cubes And Walled Offices",
                "width": 100,
                "length": 100,
                "height": 15,
            }
        }
    }
    dna.sites.create_site(payload=payload)

print_header('Create Floor')
for floor in floors:
    print_action(floor)
    if pre_check(floor) == "exist":
        print_skip()

    else:
        creation(floor)
        if post_check(floor) == "exist":
            print_pass()
        else:
            print_fail()
