import requests
import os
from dotenv import load_dotenv
import yaml
import xml.etree.ElementTree as ET
# from views import get_all_cycle

def update_release_version():
    
    endpoint = 'http://127.0.0.1:8000/api/get-release-tag/'
    response = requests.get(endpoint)
    
    if response.status_code == 200:
        cycle_list = response.json()
        unique_cycleids = set(item['cycleid'] for item in cycle_list)
        unique_cycleids_list = list(unique_cycleids)
        print(unique_cycleids_list)
        for cycle_id in unique_cycleids_list:
            #Get cycle one by one
            release = [item for item in version if item.get("cycleid") == f"{cycle_id}"]
            version = release[0]['version']
            title = release[0]['title']
            link = release[0]['stories']

            create_tag_endpoint = 'http://127.0.0.1:8000/api/release-tag/create/'

            headers = {
                'Content-Type': 'application/json'
            }

            payload = {
                "version":f'{version}',
                "cycleid":f'{cycle_id}',
                "title":f'{title}',
                "stories":f'{link}'
            }

            response = requests.post(endpoint, headers=headers, json=payload)
            print(response)
            print(cycle_id, version, title, link)

    else:
        unique_cycleids_list = []


if __name__ == '__main__':

    update_release_version()

