import requests
import os
from dotenv import load_dotenv
import yaml
import xml.etree.ElementTree as ET
from views import get_all_cycle


def get_test_amount_of_all_suites():
    #filter test case by pre-fix
    sccaws = "SCC-AWS"
    sccaz = "SCC-AZURE"
    fcpaws = "FCP-AWS"
    fcpaz = "FCP-AZURE"

    # cycles = get_all_cycle()
    # current_cycle = cycles[-1]
    current_cycle = 'FCP-C8'

    endpoint = 'http://127.0.0.1:8000/api/testresults/'
    response = requests.get(endpoint)

    if response.status_code == 200:
        testresults = response.json()
        filtered_result = [item for item in testresults if item.get("cycleid") == f"{current_cycle}"]
        
        sccaws_result = [item for item in filtered_result if sccaws in item.get("usecase", "")]
        sccaz_result = [item for item in filtered_result if sccaz in item.get("usecase", "")]
        fcpaws_result = [item for item in filtered_result if fcpaws in item.get("usecase", "")]
        fcpaz_result = [item for item in filtered_result if fcpaz in item.get("usecase", "")]

        sccaws_pass = sum(1 for pass_result in sccaws_result if pass_result.get('result') == "PASS")
        sccaws_fail = sum(1 for fail_result in sccaws_result if fail_result.get('result') == "FAIL")
        sw_total_testcases = int(sccaws_pass) + int(sccaws_fail)
        sw_percent_pass = (int(sccaws_pass) / sw_total_testcases)*100

        send_sccaws_result_stat(current_cycle, sccaws_pass, sccaws_fail, sw_percent_pass)
        sum_all_services_in_each_release(current_cycle, "SCC", "AWS", sccaws_pass, sccaws_fail)
        # print(current_cycle, sccaws_pass, sccaws_fail)

        sccaz_pass = sum(1 for pass_result in sccaz_result if pass_result.get('result') == "PASS")
        sccaz_fail = sum(1 for fail_result in sccaz_result if fail_result.get('result') == "FAIL")
        sz_total_testcases = int(sccaz_pass) + int(sccaz_fail)
        sz_percent_pass = (int(sccaz_pass) / sz_total_testcases)*100
        send_sccazure_result_stat(current_cycle, sccaz_pass, sccaz_fail, sz_percent_pass)
        sum_all_services_in_each_release(current_cycle, "SCC", "AZURE", sccaz_pass, sccaz_fail)
        # print(current_cycle, sccaz_pass, sccaz_fail)

        fcpaws_pass = sum(1 for pass_result in fcpaws_result if pass_result.get('result') == "PASS")
        fcpaws_fail = sum(1 for fail_result in fcpaws_result if fail_result.get('result') == "FAIL")
        fw_total_testcases = int(fcpaws_pass) + int(fcpaws_fail)
        fw_percent_pass = (int(fcpaws_pass) / fw_total_testcases)*100
        send_fcpaws_result_stat(current_cycle, fcpaws_pass, fcpaws_fail, fw_percent_pass)
        sum_all_services_in_each_release(current_cycle, "FCP", "AWS", fcpaws_pass, fcpaws_fail)
        # print(current_cycle, fcpaws_pass, fcpaws_fail)

        fcpaz_pass = sum(1 for pass_result in fcpaz_result if pass_result.get('result') == "PASS")
        fcpaz_fail = sum(1 for fail_result in fcpaz_result if fail_result.get('result') == "FAIL")
        fz_total_testcases = int(fcpaz_pass) + int(fcpaz_fail)
        fz_percent_pass = (int(fcpaz_pass) / fz_total_testcases)*100
        send_fcpazure_result_stat(current_cycle, fcpaz_pass, fcpaz_fail, fz_percent_pass)
        sum_all_services_in_each_release(current_cycle, "FCP", "AZURE", fcpaz_pass, fcpaz_fail)
        # print(current_cycle, fcpaz_pass, fcpaz_fail)

    else:
        response = []

def send_sccaws_result_stat(cycleid, amt_pass, amt_fail, sw_percent_pass):
    endpoint = "http://127.0.0.1:8000/api/scc-aws-result/"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "cycleid":f'{cycleid}',
        "pass_amt":f'{amt_pass}',
        "fail_amt":f'{amt_fail}',
        "percent_pass":f'{sw_percent_pass}'
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)

def send_sccazure_result_stat(cycleid, amt_pass, amt_fail, sz_percent_pass):
    endpoint = "http://127.0.0.1:8000/api/scc-azure-result/"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "cycleid":f'{cycleid}',
        "pass_amt":f'{amt_pass}',
        "fail_amt":f'{amt_fail}',
        "percent_pass":f'{sz_percent_pass}'
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)

def send_fcpaws_result_stat(cycleid, amt_pass, amt_fail, fw_percent_pass):
    endpoint = "http://127.0.0.1:8000/api/fcp-aws-result/"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "cycleid":f'{cycleid}',
        "pass_amt":f'{amt_pass}',
        "fail_amt":f'{amt_fail}',
        "percent_pass":f'{fw_percent_pass}'
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)

def send_fcpazure_result_stat(cycleid, amt_pass, amt_fail, fz_percent_pass):
    endpoint = "http://127.0.0.1:8000/api/fcp-azure-result/"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "cycleid":f'{cycleid}',
        "pass_amt":f'{amt_pass}',
        "fail_amt":f'{amt_fail}',
        "percent_pass":f'{fz_percent_pass}'
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)


def sum_all_services_in_each_release(cycleid, service_typ, cloud_provider, amt_pass, amt_fail):
    endpoint = "http://127.0.0.1:8000/api/add-release-testresult/"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "cycleid":f'{cycleid}',
        "service_typ":f'{service_typ}',
        "cloud_provider":f'{cloud_provider}',
        "pass_amt":f'{amt_pass}',
        "fail_amt":f'{amt_fail}'
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)


if __name__ == '__main__':

    get_test_amount_of_all_suites()

