import requests
import sys
import time
import os
from requests.auth import HTTPBasicAuth

GRAPHDB_ADMIN_USER = os.environ['GRAPH_DB_ADMIN_USERNAME']
GRAPHDB_ADMIN_PASSWORD = os.environ['GRAPH_DB_ADMIN_PASSWORD']

def check_triple_store_status(graphdb_url):
    url = graphdb_url + "/rest/repositories"
    try:
        response = requests.request("GET", url)
        print(response.headers)
        if response.status_code == 200:
            return True
    except:
        return False

def load_file(graphdb_url, repo_id, file_path, content_type):

    url = graphdb_url + "/repositories/" + repo_id + "/statements"
    data = open(file_path, 'rb').read()

    headers = {
        'content-type': content_type
    }

    response = requests.request("PUT", url, headers=headers, data=data,
                                auth=HTTPBasicAuth(GRAPHDB_ADMIN_USER,GRAPHDB_ADMIN_PASSWORD))
    print(response.headers)
    if response.status_code == 204:
        print("Content have be located")
        os.remove(file_path)
    else:
        print("Error loading content")

def main(graphdb_url, repo_id, file_path, content_type):
    '''
    Upload file to graphDB
    '''

    while True:
        if os.path.exists(file_path):
            load_file(graphdb_url, repo_id, file_path, content_type)
        else:
            print("Waiting for triple file to be generated. Loader sleeps for 10 seconds")
            time.sleep(5)


print("Triple loader script started")
graphdb_url = os.environ['GRAPH_DB_URL']
repo_id = os.environ['REPO_ID']
file_path = os.environ['FILE_PATH']
content_type = os.environ['CONTENT_TYPE']
if graphdb_url.endswith("/"):
    graphdb_url = graphdb_url[:-1]
print(graphdb_url)
main(graphdb_url, repo_id, file_path, content_type)
