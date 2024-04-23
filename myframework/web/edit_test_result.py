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
cycleid = 'FCP-C4'
result_id = 445



def edit_test_result(result_id):
    endpoint = "https://web-production-9df4e.up.railway.app/api/edit-testresult/{result_id}/"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "cycleid":f'{cycleid}'
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)


if __name__ == '__main__':

    while result_id < 490:
        edit_test_result(result_id)
        result_id += 1
