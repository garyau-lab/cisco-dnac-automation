# Automating Cisco DNA Center

It is a set Python script to automate Cisco DNA Center provision process.

## Prerequisites

Basic Requirement
- Python 3.x (with PIP installed)
- Cisco DNA Center API access

Install additional Python packages.
```bash
pip install -r pip-requirements.txt
```

## Usage

### Configuration files
Scripts will read the build information (e.g. credentials & build parameters) from following files, hence please update them before run the script(s).
- settings.yml
- dnac-subpool.csv
- dnac-wireless-ap.csv
- dnac-wireless-ssid.csv

### Script Files
OPTION 1 (recommended)
- Run the master shell script which will executes all Python scripts sequentially.
```python
$ run-script.sh
```

OPTION 2
- Run individual Python script to achive certain task independently. But make sure the scripts are run in a right order. It is a good reference looking at master script "run-script.sh" content.
```python
For example, sites must be created in following order
$ python create-area.py
$ python create-building.py
$ python create-floor.py
```

## Limitations

- DNAC v2.3.3.6 API doesn't support SGT creation yet, hence SGT(s) need to be created manually via DNA WebUI.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License.
