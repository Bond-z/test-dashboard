from urllib import request
from django.shortcuts import render,redirect
import requests
from django.http import JsonResponse
from subprocess import run, PIPE
import subprocess
import uuid
import os
from dotenv import load_dotenv
import yaml
import xml.etree.ElementTree as ET
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import pandas as pd
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
# from charts import get_sccaws_test_stat, get_sccazure_test_stat, get_fcpaws_test_stat, get_fcpazure_test_stat


# # Create your views here.
# zephyr_token = os.environ.get('zephyr_auth')
# usecase_path = 'test_suite.yaml'

current_cycle = "FCP-C7"

api_endpoint = "https://web-production-9df4e.up.railway.app/api/"

@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username Or Password does not exist')
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def index(request):
    
    cycles = get_all_cycle()
    current_cycle = cycles[-1]

    sort_from_latest = sorted(cycles, reverse=True)   #fcp-c7, c6, c5
    remove_latest_cycle = sort_from_latest[1:]        #fcp-c6,c5
    # first_four_cycle = remove_latest_cycle[:4]

    # get only sccaws result for all cycles
    sccaws = get_sccaws_test_stat()
    first_array_sccaws_carousel = sccaws[-5]
    filtered_sw_result = [item for item in sccaws if item.get("cycleid") == f"{current_cycle}"]
    sw_p_amt = filtered_sw_result[0]['pass_amt']
    sw_f_amt = filtered_sw_result[0]['fail_amt']

    # sw_total_testcases = int(sw_p_amt) + int(sw_f_amt)
    # sw_percent_pass = (int(sw_p_amt) / sw_total_testcases)*100

    # get scc azure test result data
    sccazure = get_sccazure_test_stat()
    first_array_sccaz_carousel = sccazure[-5]
    filtered_sa_result = [item for item in sccazure if item.get("cycleid") == f"{current_cycle}"]
    sa_p_amt = filtered_sa_result[0]['pass_amt']
    sa_f_amt = filtered_sa_result[0]['fail_amt']


    # get only fcpaws result for all cycles
    fcpaws = get_fcpaws_test_stat()
    first_array_fcpaws_carousel = fcpaws[-5]
    filtered_fw_result = [item for item in fcpaws if item.get("cycleid") == f"{current_cycle}"]
    fw_p_amt = filtered_fw_result[0]['pass_amt']
    fw_f_amt = filtered_fw_result[0]['fail_amt']

    # end gathering fcp aws data

    # get only fcpazure result for all cycles
    fcpazure = get_fcpaws_test_stat()
    first_array_fcpaz_carousel = fcpazure[-5]
    filtered_fz_result = [item for item in fcpazure if item.get("cycleid") == f"{current_cycle}"]
    fz_p_amt = filtered_fz_result[0]['pass_amt']
    fz_f_amt = filtered_fz_result[0]['fail_amt']

    # end gathering fcp azure data

    #Display all failed test cases for current sprint
    fail_testcases = get_list_of_recent_cycle_fail()

    #Display statistic pass/fail of all sprints
    barchart = bar_chart()

    #Display Pie chart for all service types in the current sprint
    charts = gennerate_chart(current_cycle, sw_p_amt, sw_f_amt, sa_p_amt, sa_f_amt, fw_p_amt, fw_f_amt, fz_p_amt, fz_f_amt)

    sccaws_stat = get_sccaws_test_stat()
    sccaws = sccaws_stat[1:]               #remove 1st array in order to display in carousel
    
    sccazure_stat = get_sccazure_test_stat()
    sccazure = sccazure_stat[1:]

    fcpaws_stat = get_fcpaws_test_stat()
    fcpaws = fcpaws_stat[1:]

    fcpazure_stat = get_fcpazure_test_stat()
    fcpazure = fcpazure_stat[1:]


    sccaws_latest_four = sccaws[-4:]
    sccaz_latest_four = sccazure[-4:]
    fcpaws_latest_four = fcpaws[-4:]
    fcpaz_latest_four = fcpazure[-4:]

    zipped_data_carousel = zip(sccaws_latest_four, sccaz_latest_four, fcpaws_latest_four, fcpaz_latest_four)
    zipped_data_table_stat = zip(sccaws_stat, sccazure_stat, fcpaws_stat, fcpazure_stat)



    endpoint = 'https://web-production-9df4e.up.railway.app/api/testresults/'
    response = requests.get(endpoint)

    if response.status_code == 200:
        testresults = response.json()
        latest_test_result = [item for item in testresults if item.get("cycleid") == f"{current_cycle}"]

    data = {
        "charts": charts,
        "cycles": cycles,
        "current_cycle": current_cycle,
        "fail_testcases": fail_testcases,
        'sw_p_amt': sw_p_amt,
        'sw_f_amt': sw_f_amt,
        'sa_p_amt': sa_p_amt,
        'sa_f_amt': sa_f_amt,
        'fw_p_amt': fw_p_amt,
        'fw_f_amt': fw_f_amt,
        'fz_p_amt': fz_p_amt,
        'fz_f_amt': fz_f_amt,
        'barchart': barchart,
        "sccaws_stat": sccaws_stat,
        "sccazure_stat": sccazure_stat,
        "fcpaws_stat": fcpaws_stat,
        "fcpazure_stat": fcpazure_stat,
        "zipped_data_carousel": zipped_data_carousel,
        "zipped_data_table_stat": zipped_data_table_stat,
        "latest_test_result": latest_test_result,
        "first_array_sccaws_carousel": first_array_sccaws_carousel,
        "first_array_sccaz_carousel": first_array_sccaz_carousel,
        "first_array_fcpaws_carousel": first_array_fcpaws_carousel,
        "first_array_fcpaz_carousel": first_array_fcpaz_carousel
    }

    return render(request,"index.html", data)


# def index(request):
#     data = {
#         "charts": "charts",
#         "cycles": "cycles"
#     }
#     return render(request, "index.html", data)

def get_sccaws_current_result(cycle):
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-scc-aws/{}/result/'.format(cycle)
    response = requests.get(endpoint)
    cycle = response.json()
    sw_p_amt = cycle[0]['pass_amt']
    sw_f_amt = cycle[0]['fail_amt']
    sw_total_testcases = int(sw_p_amt) + int(sw_f_amt)
    sw_percent_pass = (int(sw_p_amt) / sw_total_testcases)*100

    return sw_p_amt, sw_f_amt, sw_percent_pass

def get_sccaz_current_result(cycle):
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-scc-azure/{}/result/'.format(cycle)
    response = requests.get(endpoint)
    current_cycle = response.json()
    return current_cycle

def get_fcpaws_current_result(cycle):
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-fcp-aws/{}/result/'.format(cycle)
    response = requests.get(endpoint)
    current_cycle = response.json()
    return current_cycle

def get_fcpaz_current_result(cycle):
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-fcp-azure/{}/result/'.format(cycle)
    response = requests.get(endpoint)
    current_cycle = response.json()
    return current_cycle

def single_piechart(pass_amt, fail_amt):

    labels = ['Pass','Fail']
    values = [pass_amt, fail_amt]

    # pull is given as a fraction of the pie radius
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0, 0, 0.2, 0])])
    chart_html = fig.to_html(full_html=False)

    return chart_html

def get_all_testcases(request):
    endpoint = 'https://web-production-9df4e.up.railway.app/api/testcases/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        testcases = response.json()
        
    else:
        testcases = []
    return render(request, 'testcases.html', {'testcases':testcases})

def get_all_cycle():

    endpoint = 'https://web-production-9df4e.up.railway.app/api/testresults/'
    response = requests.get(endpoint)

    if response.status_code == 200:
        cycle_list = response.json()
        unique_cycleids = set(item['cycleid'] for item in cycle_list)
        unique_cycleids_list = list(unique_cycleids)
        sorted_low_to_high = sorted(unique_cycleids_list)
        # qty = len(unique_cycleids_list)
        # print(qty)
        # print(unique_cycleids_list)

    else:
        cycle_list = []
    return sorted_low_to_high    #render(request, 'dashboard.html', unique_cycleids_list)
        
def get_test_result(request):
    cycle = get_all_cycle()
    current_cycle = cycle[-1]
    # cycle_id = "FCP-C1"
    endpoint = 'https://web-production-9df4e.up.railway.app/api/testresults/'
    response = requests.get(endpoint)

    if response.status_code == 200:
        testresults = response.json()
        filtered_result = [item for item in testresults if item.get("cycleid") == f"{current_cycle}"]
        count_tc = len(filtered_result)
        print(count_tc)
        print(filtered_result)

        count_pass = sum(1 for pass_result in filtered_result if pass_result.get('result') == "PASS")
        # print(count_pass)
        
        count_fail = sum(1 for fail_result in filtered_result if fail_result.get('result') == "FAIL")
        # print(count_fail)

        #Get Pass/Fail Result by Service Types
        sccaws = get_sccaws_test_stat()
        filtered_sw_result = [item for item in sccaws if item.get("cycleid") == f"{current_cycle}"]
        sw_p_amt = filtered_sw_result[0]['pass_amt']
        sw_f_amt = filtered_sw_result[0]['fail_amt']

        # get scc azure test result data
        sccazure = get_sccazure_test_stat()
        filtered_sa_result = [item for item in sccazure if item.get("cycleid") == f"{current_cycle}"]
        sa_p_amt = filtered_sa_result[0]['pass_amt']
        sa_f_amt = filtered_sa_result[0]['fail_amt']

        # get only fcpaws result for all cycles
        fcpaws = get_fcpaws_test_stat()
        filtered_fw_result = [item for item in fcpaws if item.get("cycleid") == f"{current_cycle}"]
        fw_p_amt = filtered_fw_result[0]['pass_amt']
        fw_f_amt = filtered_fw_result[0]['fail_amt']
        # end gathering fcp aws data

        # get only fcpazure result for all cycles
        fcpazure = get_fcpaws_test_stat()
        filtered_fz_result = [item for item in fcpazure if item.get("cycleid") == f"{current_cycle}"]
        fz_p_amt = filtered_fz_result[0]['pass_amt']
        fz_f_amt = filtered_fz_result[0]['fail_amt']

        fail_testcases = get_list_of_recent_cycle_fail()


        result = {
            'testresults': filtered_result,
            'count_tc': count_tc,
            'count_pass': count_pass,
            'count_fail': count_fail,
            'cycles' : cycle,
            'sw_p_amt': sw_p_amt,
            'sw_f_amt': sw_f_amt,
            'sa_p_amt': sa_p_amt,
            'sa_f_amt': sa_f_amt,
            'fw_p_amt': fw_p_amt,
            'fw_f_amt': fw_f_amt,
            'fz_p_amt': fz_p_amt,
            'fz_f_amt': fz_f_amt,
            'fail_testcases': fail_testcases,
            'current_cycle':current_cycle
        }

    else:
        filtered_result = []
    return render(request, 'test_result.html', result)

def get_list_of_recent_cycle_fail():
    cycle = get_all_cycle()
    current_cycle = cycle[-1]

    # cycle_id = "FCP-C1"
    endpoint = 'https://web-production-9df4e.up.railway.app/api/testresults/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        testresults = response.json()
        filtered_result = [item for item in testresults if item.get("cycleid") == f"{current_cycle}"]
        fail_result = [item for item in filtered_result if item.get("result") == "FAIL"]

    return fail_result

def summarize_dashboard(request):
    sccaws = get_sccaws_test_stat()
    sccazure = get_sccazure_test_stat()
    fcpaws = get_fcpaws_test_stat()
    fcpazure = get_fcpazure_test_stat()

    zipped_data = zip(sccaws, sccazure, fcpaws, fcpazure)

    chart = bar_chart()

    data = {
        "sccaws": sccaws,
        "sccazure": sccazure,
        "fcpaws": fcpaws,
        "fcpazure": fcpazure,
        "zipped_data": zipped_data,
        "chart": chart
    }

    return render(request, 'dashboard.html', data)

def result_test_history():
    sccaws = get_sccaws_test_stat()
    sccazure = get_sccazure_test_stat()
    fcpaws = get_fcpaws_test_stat()
    fcpazure = get_fcpazure_test_stat()

    zipped_data = zip(sccaws, sccazure, fcpaws, fcpazure)

    data = {
        "sccaws": sccaws,
        "sccazure": sccazure,
        "fcpaws": fcpaws,
        "fcpazure": fcpazure,
        "zipped_data": zipped_data
    }

    return data

def sum_testresult_for_each_release():

    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-release-testresult/'
    response = requests.get(endpoint)
    data = response.json()
    print(data)
    organized_data = {}
    filtered_data = [item for item in data if item['cycleid'] == 'FCP-C1']
    print(filtered_data)
    for item in filtered_data:
        cycle_id = item['cycleid']
        print(cycle_id)
        if cycle_id not in organized_data:
            organized_data[cycle_id] = []
        organized_data[cycle_id].append(item)

def get_sccaws_test_stat():
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-scc-aws-result/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        sccaws_stat = response.json()
        
        # sort_from_latest = sorted(sccaws_stat, reverse=True)
        
    else:
        sccaws_stat = []
    return sccaws_stat

def get_sccazure_test_stat():
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-scc-azure-result/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        sccazure_stat = response.json()
        
    else:
        sccazure_stat = []
    return sccazure_stat

def get_fcpaws_test_stat():
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-fcp-aws-result/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        fcpaws_stat = response.json()
        
    else:
        fcpaws_stat = []
    return fcpaws_stat

def get_fcpazure_test_stat():
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-fcp-azure-result/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        fcpazure_stat = response.json()
        
    else:
        fcpazure_stat = []
    return fcpazure_stat

#Get all latest four cycles
def get_last_four_fcpazure_result():
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-fcp-azure-result/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        fcpazure_stat = response.json()

        # Sort the list of dictionaries based on the "create" key
        sorted_data = sorted(fcpazure_stat, key=lambda x: x['create'])

        # Keep the last four items
        fcpazure_latest_four = sorted_data[-4:]
        
    else:
        fcpazure_stat = []
    return fcpazure_latest_four

def get_last_four_fcpaws_result():
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-fcp-aws-result/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        fcpaws_stat = response.json()

        # Sort the list of dictionaries based on the "create" key
        sorted_data = sorted(fcpaws_stat, key=lambda x: x['create'])

        # Keep the last four items
        fcpaws_latest_four = sorted_data[-4:]
        
    else:
        fcpaws_stat = []
    return fcpaws_latest_four

def get_last_four_sccaws_result():
    # endpoint = 'https://web-production-9df4e.up.railway.app/api/get-scc-aws-result/'
    # response = requests.get(endpoint)
    response = get_sccaws_test_stat()
    if response.status_code == 200:
        sccaws_stat = response.json()

        # Sort the list of dictionaries based on the "create" key
        sorted_data = sorted(sccaws_stat, key=lambda x: x['create'])

        # Keep the last four items
        sccaws_latest_four = sorted_data[-4:]
        
    else:
        sccaws_stat = []
    
    return sccaws_latest_four

def get_last_four_sccazure_result():
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-scc-azure-result/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        sccazure_stat = response.json()

        # Sort the list of dictionaries based on the "create" key
        sorted_data = sorted(sccazure_stat, key=lambda x: x['create'])

        # Keep the last four items
        sccazure_latest_four = sorted_data[-4:]
        
    else:
        sccazure_stat = []
    return sccazure_latest_four

@login_required(login_url='/login')
def get_testresult_by_cycleid(request, cycle_id):
    cycle = get_all_cycle()
    endpoint = 'https://web-production-9df4e.up.railway.app/api/testresults/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        testresults = response.json()
        filtered_result = [item for item in testresults if item.get("cycleid") == f"{cycle_id}"]
        count_tc = len(filtered_result)
        print(count_tc)
        print(filtered_result)

        count_pass = sum(1 for pass_result in filtered_result if pass_result.get('result') == "PASS")
        # print(count_pass)
        
        count_fail = sum(1 for fail_result in filtered_result if fail_result.get('result') == "FAIL")
        # print(count_fail)

        #Get Pass/Fail Result by Service Types
        sccaws = get_sccaws_test_stat()
        filtered_sw_result = [item for item in sccaws if item.get("cycleid") == f"{cycle_id}"]
        sw_p_amt = filtered_sw_result[0]['pass_amt']
        sw_f_amt = filtered_sw_result[0]['fail_amt']

        # get scc azure test result data
        sccazure = get_sccazure_test_stat()
        filtered_sa_result = [item for item in sccazure if item.get("cycleid") == f"{cycle_id}"]
        sa_p_amt = filtered_sa_result[0]['pass_amt']
        sa_f_amt = filtered_sa_result[0]['fail_amt']

        # get only fcpaws result for all cycles
        fcpaws = get_fcpaws_test_stat()
        filtered_fw_result = [item for item in fcpaws if item.get("cycleid") == f"{cycle_id}"]
        fw_p_amt = filtered_fw_result[0]['pass_amt']
        fw_f_amt = filtered_fw_result[0]['fail_amt']
        # end gathering fcp aws data

        # get only fcpazure result for all cycles
        fcpazure = get_fcpaws_test_stat()
        filtered_fz_result = [item for item in fcpazure if item.get("cycleid") == f"{cycle_id}"]
        fz_p_amt = filtered_fz_result[0]['pass_amt']
        fz_f_amt = filtered_fz_result[0]['fail_amt']

        fail_testcases = get_list_of_recent_cycle_fail()

        pie = single_piechart(count_pass, count_fail)

        version, title, link = get_release_version(cycle_id)



        result = {
            'testresults': filtered_result,
            'count_tc': count_tc,
            'count_pass': count_pass,
            'count_fail': count_fail,
            'cycles' : cycle,
            'sw_p_amt': sw_p_amt,
            'sw_f_amt': sw_f_amt,
            'sa_p_amt': sa_p_amt,
            'sa_f_amt': sa_f_amt,
            'fw_p_amt': fw_p_amt,
            'fw_f_amt': fw_f_amt,
            'fz_p_amt': fz_p_amt,
            'fz_f_amt': fz_f_amt,
            'fail_testcases': fail_testcases,
            'pie': pie,
            'version': version,
            'title': title,
            'link': link
        }


    else:
        filtered_result = []
    return render(request, 'cycleid.html', result)

def get_release_version(cycle_id):
    endpoint = 'https://web-production-9df4e.up.railway.app/api/get-release-tag/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        version = response.json()
        release = [item for item in version if item.get("cycleid") == f"{cycle_id}"]
        version = release[0]['version']
        title = release[0]['title']
        link = release[0]['stories']
        
    else:
        release = []

    return version, title, link

def bar_chart():
    # Generate sample data for the bar chart
    cycles = get_all_cycle()
    release = []
    r_pass = []
    r_fail = []
    testcases = []

    for cycle in cycles:
        release.append(cycle)
        
        tc, rpass, rfail = get_cycleid_testresult(cycle)
        r_pass.append(rpass)
        r_fail.append(rfail)
        testcases.append(tc)

    data = {
        'Release': release,
        'Pass': r_pass,
        'Fail': r_fail
    }

    # Create a bar chart using Plotly Express
    fig = px.bar(data, x='Release', y=['Pass', 'Fail'], title='', labels={'Pass': 'Value 1', 'Fail': 'Value 2'},
             color_discrete_map={'Pass': 'rgb(0, 128, 0)', 'Fail': 'rgb(255, 34, 0)'},  # Adjust bar colors
             width=700, height=500)

    # Convert the Plotly figure to HTML
    chart_html = fig.to_html(full_html=False)

    # Render the HTML template with the chart
    return chart_html


def gennerate_chart(cycleid, sw_pass, sw_fail, sz_pass, sz_fail, fw_pass, fw_fail, fz_pass, fz_fail):

    labels = ['PASS', 'FAIL']
    sccaws = [f'{sw_pass}', f'{sw_fail}']
    sccazure = [f'{sz_pass}', f'{sz_fail}']
    fcpaws = [f'{fw_pass}', f'{fw_fail}']
    fcpazure = [f'{fz_pass}', f'{fz_fail}']


    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=4, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'} ]])
    fig.add_trace(go.Pie(labels=labels, values=sccaws, name="SCC-AWS"),
                1, 1)
    fig.add_trace(go.Pie(labels=labels, values=sccazure, name="SCC-AZURE"),  
                1, 2)
    fig.add_trace(go.Pie(labels=labels, values=fcpaws, name="FCP-AWS"),
                1, 3)
    fig.add_trace(go.Pie(labels=labels, values=fcpazure, name="FCP-AZURE"),
                1, 4)

    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    charts = fig.update_layout(
            title_text="Summarized of Regression Test Result Of Cycle - " f'{cycleid}', 
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='SCC-AWS', x=0.08, y=0.5, font_size=11, showarrow=False), 
                        dict(text='SCC-AZURE', x=0.37, y=0.5, font_size=11, showarrow=False),
                        dict(text='FCP-AWS', x=0.63, y=0.5, font_size=11, showarrow=False),
                        dict(text='FCP-AZURE', x=0.93, y=0.5, font_size=11, showarrow=False)])
    # fig.show()
    chart_html = charts.to_html(full_html=False)
    return chart_html

def get_cycleid_testresult(cycle_id):

    endpoint = 'https://web-production-9df4e.up.railway.app/api/testresults/'
    response = requests.get(endpoint)
    if response.status_code == 200:
        testresults = response.json()
        filtered_result = [item for item in testresults if item.get("cycleid") == f"{cycle_id}"]
        count_tc = len(filtered_result)
        # print(count_tc)
        # print(filtered_result)

        count_pass = sum(1 for pass_result in filtered_result if pass_result.get('result') == "PASS")
        # print(count_pass)
        
        count_fail = sum(1 for fail_result in filtered_result if fail_result.get('result') == "FAIL")
        # print(count_fail)

    else:
        filtered_result = []

    return count_tc, count_pass, count_fail

#Function: send test cases to 
def create_testcases(testid, usecase):
    endpoint = "https://web-production-9df4e.up.railway.app/api/add-testcase/"


    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "testcaseid":f'{testid}',
        "usecase":f'{usecase}'
    }

    response = requests.post(endpoint, headers=headers, json=payload)
    print(response)

#Edit test case
def update_testcases(id, testid, usecase):
    endpoint = "https://web-production-9df4e.up.railway.app/api/update-testcase/f'{id}'"

    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        "testcaseid":"AUTHEN-1",
        "usecase":"Get Bearer Token to call other endpoint - edit"
    }

    response = requests.put(endpoint, headers=headers, json=payload)
    print(response)






    


if __name__ == '__main__':
#     create_testcases()
#     update_testcases()

    cycles = get_all_cycle()
    print(cycles)







