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


def pre_check(device):
    hostname1 = device['hostname'].split(".")[0]
    try:
        dna_devices = dna.devices.get_device_list()
        for i in dna_devices['response']:
            hostname2 = i['hostname'].split(".")[0]
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
        "type": "NETWORK_DEVICE",
        "ipAddress": [device['ip_address']],
        "cliTransport": set_dict['cli_protocol'],
        "userName": set_dict['cli_username'],
        "password": set_dict['cli_password'],
        "enablePassword": set_dict['cli_enable'],
        "snmpVersion": set_dict['snmp_version'],
        "snmpMode": set_dict['snmp_mode'],
        "snmpUserName": set_dict['snmp_username'],
        "snmpAuthProtocol": set_dict['snmp_auth_protocol'],
        "snmpAuthPassphrase": set_dict['snmp_auth_passphrase'],
        "snmpPrivProtocol": set_dict['snmp_priv_protocol'],
        "snmpPrivPassphrase": set_dict['snmp_priv_passphrase']
    }
    if device['netconf'] == "yes":
        payload['netconfPort'] = str(set_dict['netconf_port'])
    dna.devices.add_device(payload=payload)

print_header('Add Device')
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
