import time
import yaml, json
from dnacentersdk import api
from print_report import *

with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check():
    try:
        response = dna.sda.get_default_authentication_profile(site_name_hierarchy=site_hierarchy)
        if response['authenticateTemplateName'] == "No Authentication":
            return ("exist")
        else:
            return
    except:
        return

def post_check():
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        if pre_check() == "exist":
            return ("exist")

def creation():
    payload = [
        {
            "siteNameHierarchy": site_hierarchy,
            "authenticateTemplateName": "No Authentication"
        }
    ]
    dna.sda.add_default_authentication_profile(payload=payload)

print_header('Add Default Authentication Profile to Fabric Site')
print_action(set_dict['site_building'])
if pre_check() == "exist":
    print_skip()
else:
    creation()
    if post_check() == "exist":
        print_pass()
    else:
        print_fail()
