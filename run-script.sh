tput bold; echo "CREATE VIRTUAL NETWORK"; tput sgr0
python3 create-vn.py

echo; tput bold; echo "CREATE WIRELESS NETWORK"; tput sgr0
python3 create-enterprise-ssid.py

echo; tput bold; echo "CREATE SITE"; tput sgr0
python3 create-area.py
python3 create-building.py
python3 create-floor.py

echo; tput bold; echo "CREATE IP ADDRESS POOL"; tput sgr0
python3 create-global-pool.py
python3 create-subpool.py

echo; tput bold; echo "CREATE WIRELESS PROFILE"; tput sgr0
python3 create-wireless-profile-bldg.py
python3 create-wireless-profile-floor.py

echo; tput bold; echo "SETUP FABRIC SITE"; tput sgr0
python3 add-sda-site.py
python3 add-default-auth-profile.py
python3 add-vn-to-sda.py
python3 add-subpool-to-vn.py

echo; tput bold; echo "ADD DEVICE"; tput sgr0
python3 add-device.py
python3 provision-device.py

echo; tput bold; echo "ADD AND CONFIGURE FABRIC DEVICE"; tput sgr0
python3 add-sda-ip-transit.py
python3 add-sda-in-a-box-node.py
#python3 add-sda-wlc-node.py
read -p "Please add fabric WLC role manually, then press ENTER to continue ..."
python3 add-sda-ssid-ippool-mapping.py
python3 add-sda-port-asgmt-user.py
python3 add-sda-port-asgmt-ap.py