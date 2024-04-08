import xml.etree.ElementTree as ET
import datetime
import time
import pandas
import os
from dotenv import load_dotenv
import glob
import requests
import re
import yaml
from all_testcase import *
from zephyr import *
from views import create_testcases


#Create column
testcaseid_pattern = r"Testcase ID:.*"
postman_pattern = r"Postman:.*"
servicenow_pattern = r"Servicenow:.*"
customerui_pattern = r"Customer UI:.*"
automation_pattern = r"Automation:.*"
cloudprovider_pattern = r"Cloud Privder:.*"
endpoint_pattern = r"Endpoint:.*"
method_pattern = r"Method:.*"
usecase_pattern = r"Use case:.*"
standardrun_pattern = r"Standard_Run:.*"
fasttrackrun_pattern = r"Fast Track Run:.*"
accounttype_pattern = r"Account Type:.*"
servicetype_pattern = r"Service type:.*"
url_pattern = r"URL:.*"
body_pattern = r"Body:.*"
response_pattern = r"Response: \|([\s\S]+)"
result_pattern = r"Result:.*"
remark_pattern = r"Remark:.*"
jira_pattern = r"JIRA:.*"
ghe_pattern = r"GHE:.*"


if __name__ == '__main__':

    testcaseid = re.findall(testcaseid_pattern, input_text)
    postman = re.findall(postman_pattern, input_text)
    servicenow = re.findall(servicenow_pattern, input_text)
    customerui = re.findall(customerui_pattern, input_text)
    automation = re.findall(automation_pattern, input_text)
    cloudprovider = re.findall(cloudprovider_pattern, input_text)
    endpoint = re.findall(endpoint_pattern, input_text)
    method = re.findall(method_pattern, input_text)
    usecase = re.findall(usecase_pattern, input_text)
    standardrun = re.findall(standardrun_pattern, input_text)
    fasttrackrun = re.findall(fasttrackrun_pattern, input_text)
    accounttype = re.findall(accounttype_pattern, input_text)
    servicetype = re.findall(servicetype_pattern, input_text)
    url = re.findall(url_pattern, input_text)
    body = re.findall(body_pattern, input_text)
    response = re.findall(response_pattern, input_text)
    result = re.findall(result_pattern, input_text)
    remark = re.findall(remark_pattern, input_text)
    jira = re.findall(jira_pattern, input_text)
    ghe = re.findall(ghe_pattern, input_text)


    data = { 'TestcaseID': testcaseid, 'Usecase': usecase }
    df = pandas.DataFrame(data)
    df['combine'] = df[['TestcaseID', 'Usecase']].values.tolist()
    df = df.loc[:,"combine"]

    # s = df.to_string()
    testcase_len = len(df)
    print("Total amount of test cases are : {}".format(testcase_len))
    # print(s)

    testid = 286                                                      # zephyr test case id start from no. FCP-T262, each test case will be mapped with zephyr id for only when we update
    #testid are missing from 280 - 285
    #so we need to run 2 times, 1st from 262-279, 2nd from 286 onward
    for i in df:
        test_id = i[0].strip('TestcaseID: ')
        testcase = i[1].strip('Usecase: ')
        topic = test_id + ' ' + testcase
        print(topic)                                                                  #display all test cases in regression package

        create_testcases(test_id, testcase)

