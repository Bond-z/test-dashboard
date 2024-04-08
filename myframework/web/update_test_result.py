import requests
import os
from dotenv import load_dotenv
import yaml
import xml.etree.ElementTree as ET

sccaws = './test_result/scc_aws_log.xml'
sccazure = './test_result/scc_azure_log.xml'
fcpaws = './test_result/fcp_aws_log.xml'
fcpazure = './test_result/fcp_azure_log.xml'

xml_paths = [f'{fcpaws}', f'{fcpazure}', f'{sccaws}', f'{sccazure}']
zephyrid_path = 'test_id.yaml'
usecase_path = 'test_suite.yaml'
cycleid = 'FCP-C8'

def get_result_and_update_testresult(root):

    for item in root.findall('./statistics/tag/stat'):

        testcase_id = item.text
        status_pass = item.attrib["pass"]
        status_fail = item.attrib["fail"]

        try:
            if status_pass == "1":

                zephyr_id = get_zephyrid_from_yaml(testcase_id)     # Map data dict "FCP-T262"
                usecase = get_testcases_from_yaml(zephyr_id)

                if usecase is not None:
                    create_test_cycle_with_result(cycleid, zephyr_id, usecase, "PASS")
                    print("{}, {} : {} : PASS".format(cycleid, zephyr_id, usecase))
                else:
                    print(f"Key '{zephyr_id}' is None")

            elif status_fail == "1":

                zephyr_id = get_zephyrid_from_yaml(testcase_id)      # Map data dict
                usecase = get_testcases_from_yaml(zephyr_id)
                if usecase is not None:
                    create_test_cycle_with_result(cycleid, zephyr_id, usecase, "FAIL")
                    print("{}, {} : {} : FAIL".format(cycleid, zephyr_id, usecase))
                else:
                    print(f"Key '{zephyr_id}' is None")

        except Exception as e:
            print('Error: ', str(e))

def get_zephyrid_from_yaml(key):
    try:
        variables = read_yaml(zephyrid_path)
        value = variables.get(key)
        if value is not None:
            # print(f"Value for key '{key}': {value}")
            return value
        else:
            print(f"Key '{key}' not found in YAML file.")
    except FileNotFoundError:
        print(f"Error: File '{zephyrid_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")

def read_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def get_testcases_from_yaml(key):

    try:
        variables = read_yaml(usecase_path)
        value = variables.get(key)
        if value is not None:
            # print(f"Value for key '{key}': {value}")
            # print(f"{key}:{value}")
            return value
        else:
            print(f"Key '{key}' not found in YAML file.")
    except FileNotFoundError:
        print(f"Error: File '{usecase_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")

def create_test_cycle_with_result(cycleid, zephyr_id, usecase, result):
    endpoint = "http://127.0.0.1:8000/api/add-testresult/"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "cycleid":f'{cycleid}',
        "testcaseid":f'{zephyr_id}',
        "usecase":f'{usecase}',
        "result":f'{result}',
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)


if __name__ == '__main__':

    for log in xml_paths:
        tree = ET.parse(log)
        root = tree.getroot()
        get_result_and_update_testresult(root)

    # create_test_cycle_with_result(cycleid, "FCP-T262", "AUTHEN-1 Get Bearer Token to call other endpoint", "PASS")