import xml.etree.ElementTree as ET
import datetime
import time
import pandas
import os
from dotenv import load_dotenv
import glob
import requests
import json
import yaml
import certifi
import ssl




sccaws = './test_result/scc_aws_log.xml'
sccazure = './test_result/scc_azure_log.xml'
fcpazure = './test_result/fcp_azure_log.xml'
fcpaws = './test_result/fcp_aws_log.xml'

xml_paths = [f'{sccaws}', f'{sccazure}', f'{fcpazure}', f'{fcpaws}']


# yaml_path = 'test_suite.yaml'
yaml_path = 'test_id.yaml'

test_cycle = "FCP-C24"    #Need to change test cycle id very sprint and everytime that we create test plan and test cycle

date_time = datetime.datetime.now()

zephyr_token = os.environ.get('zephyr_auth')

headers = {
    'Authorization': 'Bearer ' + zephyr_token,
    'Content-Type': 'application/json'
}


def get_result(root):
    testcaseId = []
    result = []

    for item in root.findall('./statistics/tag/stat'):

        testcase_id = item.text
        status_pass = item.attrib["pass"]
        status_fail = item.attrib["fail"]

        try:
            if status_pass == "1":
                testcaseId.append(testcase_id)
                result.append("pass")
                print(f'{testcase_id} : Pass')

                zephyr_id = get_value_from_yaml(testcase_id)     # Map data dict
                update_test_result(zephyr_id, "Pass")            # Send test result on zephyr when pass

            elif status_fail == "1":
                testcaseId.append(testcase_id)
                result.append("fail")
                print(f'{testcase_id} : Fail')

                zephyr_id = get_value_from_yaml(testcase_id)      # Map data dict
                update_test_result(zephyr_id, "Fail")             # Send test result on zephyr when fail

        except Exception as e:
            print('Error: ', str(e))

    df = pandas.DataFrame(testcaseId, columns=['ID'])
    test_result = df.assign(Results = result)

    return test_result

def update_test_result(test_id, test_result):

    # API endpoint URL
    url = "https://jmp.allianz.net/rest/atm/1.0/"
    uri = "testrun/{}/testcase/{}/testresult".format(test_cycle, test_id)
    endpoint = url+uri

    # Request payload
    payload = {
        "projectKey": "FCP",
        "testCaseKey": "{}".format(test_id),
        "status": "{}".format(test_result)
    }

    # Send the POST request with Basic Authentication
    response = requests.post(endpoint, headers=headers, json=payload)

    return response

#Create test cases
def create_new_testcase(usecase, test_id, folder):
    url = "https://jmp.allianz.net/rest/atm/1.0/"
    uri = "testcase"
    endpoint = url+uri

    headers = {
        'Authorization': 'Bearer ' + zephyr_token,
        'Content-Type': 'application/json'
    }

    # Request payload
    payload = {
            "projectKey": "FCP",
            "name": "{}".format(usecase),
            "labels": [f"{test_id}"],
            "folder": "{}".format(folder)
        }
    time.sleep(2)
    response = requests.post(endpoint, headers=headers, json=payload)

    return response

def get_testcases():
    key = "FCP"
    url = "https://jmp.allianz.net/rest/atm/1.0/"
    uri = f'testcase/search?query=projectKey = {key}&fields=key,name,labels,folder'

    headers = {
        'Authorization': f'Bearer {zephyr_token}',
        'Content-Type': 'application/json'
    }

    endpoint = url+uri
    response = requests.get(endpoint, headers=headers)

    return response.json()


def list_testcase(json_data):          #displayed like : FCP-T467 : FCP-AZURE-CIDR-1 Add existing CIDR to CIDRAllocated table for your test account and correct region

    if json_data:
        num = len(json_data)
        for i in range (num):

            id = json_data[i].get('key')
            tc = json_data[i].get('name')
            # path = json_data[i].get('folder')
            print("{} : {}".format(id, tc))

            # if path == "/hybrid-cloud/network/scc/aws":          #fillter test cases in specific folder
            #     print("{} : {}".format(id, tc))

def get_testcase_key(json_data):
    if json_data:
        num = len(json_data)
        print(num)

        for i in range (num):
            id = json_data[i].get('key')
            labels = json_data[i].get('labels')
            print("{} : {}".format(labels[0], id))

            # if path == "/hybrid-cloud/network/scc/aws":         #looking for test cases in specific folder
            #     print("{}".format(id))

            # return id

def update_testcase(testcasekey, name, folder, test_id):
    url = "https://jmp.allianz.net/rest/atm/1.0/"
    uri = f'testcase/{testcasekey}'

    headers = {
        'Authorization': f'Bearer {zephyr_token}',
        'Content-Type': 'application/json'
    }

    payload = {
            "name": "{}".format(name),
            "folder": "{}".format(folder),
            "labels": [f"{test_id}"]
        }

    endpoint = url+uri
    time.sleep(2)
    response = requests.put(endpoint, headers=headers, json=payload)

    # print(zephyr_token, response, endpoint, payload, test_id)
    return response


def delete_testcase(testcasekey):
    url = "https://jmp.allianz.net/rest/atm/1.0/"
    uri = f'testcase/{testcasekey}'

    endpoint = url+uri
    time.sleep(1)
    response = requests.delete(endpoint, headers=headers)

def map_id():

    testcasekey = 262
    while testcasekey <= 270:
        testid = f'FCP-T{testcasekey}'
        url = "https://jmp.allianz.net/rest/atm/1.0/"
        uri = f'testcase/{testid}'
        endpoint = url+uri
        print(endpoint)
        # response = requests.get(endpoint, headers=headers)
        # json_data = response.json()
        # id = json_data.get('key')
        # name = json_data.get('name')

        # if tag in name:    #FCP-AZURE-ACCOUNT-1 in
        #     #
        #     print(id)

        testcasekey += 1


def read_yaml(yaml_path):
    with open(yaml_path, 'r') as file:
        data = yaml.safe_load(file)
    return data

def get_value_from_yaml(key):
    try:
        variables = read_yaml(yaml_path)
        value = variables.get(key)
        if value is not None:
            # print(f"Value for key '{key}': {value}")
            return value
        else:
            print(f"Key '{key}' not found in YAML file.")
    except FileNotFoundError:
        print(f"Error: File '{yaml_path}' not found.")
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")

def get_test_cycle():
    key = "FCP"
    url = "https://jmp.allianz.net/rest/atm/1.0/"
    uri = f'testrun/FCP-C23'

    headers = {
        'Authorization': f'Bearer {zephyr_token}',
        'Content-Type': 'application/json'
    }

    endpoint = url+uri
    response = requests.get(endpoint, headers=headers)

    return response.json()

def get_test_result_from_zephyr():
    key = "FCP"
    url = "https://jmp.allianz.net/rest/atm/1.0/"
    uri = f'testrun/FCP-C23'

    headers = {
        'Authorization': f'Bearer {zephyr_token}',
        'Content-Type': 'application/json'
    }

    endpoint = url+uri
    response = requests.get(endpoint, headers=headers)
    json_data = response.json()

    if json_data:
       
        count = json_data.get('testCaseCount')
        testcases = json_data.get('items')

        for i in range(count):
            testCaseKey = testcases[i].get('testCaseKey')
            # testResult = testcases[i].get('status')
            print("{}".format(testCaseKey))

            #update test result to django db
            
zephyrid = ["FCP-T361","FCP-T362","FCP-T469","FCP-T470","FCP-T360","FCP-T359","FCP-T363","FCP-T435","FCP-T444","FCP-T445","FCP-T436","FCP-T437","FCP-T438","FCP-T439","FCP-T440","FCP-T441","FCP-T442","FCP-T443","FCP-T420","FCP-T429","FCP-T430","FCP-T431","FCP-T432","FCP-T433","FCP-T434","FCP-T421","FCP-T422","FCP-T423","FCP-T424","FCP-T425","FCP-T426","FCP-T427","FCP-T428","FCP-T413","FCP-T414","FCP-T415","FCP-T416","FCP-T417","FCP-T418","FCP-T419","FCP-T404","FCP-T405","FCP-T406","FCP-T407","FCP-T408","FCP-T409","FCP-T410","FCP-T411","FCP-T412","FCP-T262","FCP-T263","FCP-T364","FCP-T373","FCP-T374","FCP-T365","FCP-T366","FCP-T367","FCP-T368","FCP-T369","FCP-T370","FCP-T371","FCP-T372","FCP-T375","FCP-T384","FCP-T385","FCP-T376","FCP-T377","FCP-T378","FCP-T379","FCP-T380","FCP-T381","FCP-T382","FCP-T383","FCP-T386","FCP-T387","FCP-T458","FCP-T459","FCP-T460","FCP-T461","FCP-T462","FCP-T463","FCP-T464","FCP-T465","FCP-T466","FCP-T467","FCP-T347","FCP-T348","FCP-T349","FCP-T350","FCP-T351","FCP-T357","FCP-T358","FCP-T289","FCP-T290","FCP-T291","FCP-T292","FCP-T293","FCP-T294","FCP-T295","FCP-T296","FCP-T298","FCP-T299","FCP-T319","FCP-T320","FCP-T321","FCP-T322","FCP-T323","FCP-T325","FCP-T446","FCP-T455","FCP-T447","FCP-T448","FCP-T449","FCP-T450","FCP-T451","FCP-T452","FCP-T453","FCP-T454","FCP-T456","FCP-T457","FCP-T332","FCP-T333","FCP-T334","FCP-T335","FCP-T336","FCP-T337","FCP-T338","FCP-T339","FCP-T340","FCP-T341","FCP-T342","FCP-T264","FCP-T273","FCP-T274","FCP-T275","FCP-T276","FCP-T277","FCP-T265","FCP-T266","FCP-T267","FCP-T268","FCP-T269","FCP-T270","FCP-T271","FCP-T272","FCP-T279","FCP-T286","FCP-T300","FCP-T309","FCP-T310","FCP-T311","FCP-T301","FCP-T302","FCP-T303","FCP-T304","FCP-T305","FCP-T306","FCP-T307","FCP-T308","FCP-T315","FCP-T316"]

def get_testcases_from_yaml():
    for key in zephyrid:

        try:
            variables = read_yaml(yaml_path)
            value = variables.get(key)
            if value is not None:
                # print(f"Value for key '{key}': {value}")
                print(f"{key}:{value}")
                # return value
            else:
                print(f"Key '{key}' not found in YAML file.")
        except FileNotFoundError:
            print(f"Error: File '{yaml_path}' not found.")
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")

if __name__ == '__main__':
    for log in xml_paths:
        tree = ET.parse(log)
        root = tree.getroot()
        result = get_result(root)


    # # GET ALL TEST CASES #
    # response = get_testcases()
    # data = list_testcase(response)
    # print(data)

    # GET ONLY TEST KEY #
    # response = get_testcases()
    # get_testcase_key(response)



    # DELETE TEST CASES
    # for id in test_id:
    #     delete_testcase(id)
    #     print("delete {}".format(id))

    # map_id()

    #Test update test case
    # folder = "/scc-api/others"
    # testcasekey = "FCP-T337"
    # name = "create new test case"
    # test_id = "FCP-AWS-ACCOUNT-DELETE-2"
    # # update_testcase(testcasekey, name, folder, test_id)

    # create_new_testcase(name, test_id, folder)


    # response = get_test_cycle()
    # get_test_result_from_zephyr()

    # get_testcases_from_yaml()

    # update_test_result("FCP-T263", "Pass")
    # result = get_testcases()
    # print(result)