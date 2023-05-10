import time
import yaml, json, csv
from dnacentersdk import api
from print_report import *

with open('settings.yml') as info:
    set_dict = yaml.safe_load(info)

dna = api.DNACenterAPI(base_url=(set_dict['dnac_url']),
    username=(set_dict['dnac_username']), password=(set_dict['dnac_password']), verify=False)

# Read CSV file as an array of dictionary
port_dict = []
with open('dnac-port-assignment.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)
    for row in csv_reader:
        row_data = {key: value for key, value in zip(headers, row)}
        port_dict.append(row_data)


site_hierarchy = set_dict['site_parent']+"/"+set_dict['site_area']+"/"+set_dict['site_building']

def pre_check(mgmt_ip, interface_name, port):
    try:
        response = dna.sda.get_port_assignment_for_access_point(device_management_ip_address=mgmt_ip, interface_name=interface_name)
        if response['dataIpAddressPoolName'] == port['data_pool'] and response['authenticateTemplateName'] == port['auth_template']:
            return ("same")
        else:
            return ("different")
    except:
        response = dna.sda.get_port_assignment_for_user_device(device_management_ip_address=mgmt_ip, interface_name=interface_name)
        if response['status'] == "success":
            return ("different")

def post_check(mgmt_ip, interface_name, port):
    for i in range(set_dict['verify_retry_normal']):
        time.sleep(set_dict['verify_delay'])
        result = pre_check(mgmt_ip, interface_name, port)
        if result != None:
            return (result)

def port_reset(mgmt_ip, interface_name):
    try:
        dna.sda.delete_port_assignment_for_user_device(device_management_ip_address=mgmt_ip, interface_name=interface_name)
        while 1 < 2:
            time.sleep(set_dict['verify_delay'])
            try:
                response = dna.sda.get_port_assignment_for_user_device(device_management_ip_address=mgmt_ip, interface_name=interface_name)
                if response['status'] == "failed":
                    return
            except:
                continue
    except:
        dna.sda.delete_port_assignment_for_access_point(device_management_ip_address=mgmt_ip, interface_name=interface_name)
        while 1 < 2:
            time.sleep(set_dict['verify_delay'])
            try:
                response = dna.sda.get_port_assignment_for_access_point(device_management_ip_address=mgmt_ip, interface_name=interface_name)
            except:
                return

def creation(mgmt_ip, interface_name, port):
    payload = {
        "siteNameHierarchy": site_hierarchy,
        "deviceManagementIpAddress": mgmt_ip,
        "interfaceName": interface_name,
        "dataIpAddressPoolName": port['data_pool'],
        "authenticateTemplateName": port['auth_template']
    }
    dna.sda.add_port_assignment_for_access_point(payload=payload)

def get_mgmt_ip(port):
    hostname1 = port['device_name']
    dna_devices = dna.devices.get_device_list()
    for i in dna_devices['response']:
        hostname2 = i['hostname'].split(".")[0]
        if hostname1 == hostname2:
            return (i['managementIpAddress'])

def construct_intf_list(port):
    intf_names = []

    if "-" in port['port_name']:
        port1 = port['port_name'].split("-")[0]
        port2 = port['port_name'].split("-")[1]

        intf_prefix = port1.rsplit("/",1)[0] 
        intf_start = int(port1.rsplit("/",1)[1])
        intf_end = int(port2.rsplit("/",1)[1])
        for i in range (intf_start, intf_end):
            intf_names.append(intf_prefix+"/"+str(i))
        return (intf_names)

    if "," in port['port_name']:
        intf_names = port['port_name'].split(",")
        return (intf_names)

    intf_names.append(port['port_name'])
    return (intf_names)

print_header('Perform port assigment for AP')
for port in port_dict:
    if port['port_type'] == "ap":
        mgmt_ip = get_mgmt_ip(port)
        intf_names = construct_intf_list(port)

        # Start
        for i in intf_names:
            print_action(i+" ["+port['data_pool']+"]")

            if port['supersede'] != "yes":
                pre_check_result = pre_check(mgmt_ip, i, port)
                if pre_check_result == "same":
                    print_skip()
                elif pre_check_result == "different":
                    print_skip_custom("Skip, port with other config")
                elif pre_check_result == None:
                    creation(mgmt_ip, i, port)
                    if post_check(mgmt_ip, i, port) != None:
                        print_pass()
                    else:
                        print_fail()
            
            elif port['supersede'] == "yes":
                pre_check_result = pre_check(mgmt_ip, i, port)
                if pre_check_result == "same":
                    print_skip()
                elif pre_check_result == "different":
                    print_status("Resetting port")
                    port_reset(mgmt_ip, i)
                    print_status("Configuring port")                    
                    creation(mgmt_ip, i, port)
                    if post_check(mgmt_ip, i, port) != None:
                        print_pass_custom("Config superseded")
                    else:
                        print_fail()
                elif pre_check_result == None:
                    creation(mgmt_ip, i, port)
                    if post_check(mgmt_ip, i, port) != None:
                        print_pass()
                    else:
                        print_fail()




