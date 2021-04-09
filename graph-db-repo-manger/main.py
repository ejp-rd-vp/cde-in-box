import requests
import sys
import chevron
import time

def check_triple_store_status(graphdb_url):
    url = graphdb_url + "/rest/repositories"
    try:
        response = requests.request("GET", url)
        return True
    except:
        return False


def check_repository(graphdb_url, repo_id):

    url = graphdb_url + "/rest/repositories/" + repo_id
    does_repo_exists = False
    headers = {'Accept': "text/turtle"}

    response = requests.request("GET", url, headers=headers)
    print(response.headers)

    if response.status_code == 200:
        does_repo_exists = True

    return does_repo_exists

def create_repository(graphdb_url, repo_id, repo_description):

    while not check_triple_store_status(graphdb_url):
        print("Waiting for triple store come online")
        time.sleep(5)

    if not check_repository(graphdb_url, repo_id):
        repo_config = None
        with open('templates/repo-config.mustache', 'r') as f:
            repo_config = chevron.render(f, {'id': repo_id, 'description': repo_description})

        file = open("config.ttl", "w")
        file.write(repo_config)
        file.close()

        config_file = open("config.ttl", "rb")
        url = graphdb_url + "/rest/repositories"

        response = requests.request("POST", url, files={"config": config_file})
        print(response.headers)
        if response.status_code == 201:
            print(repo_id + " repository has be created")
    else:
        print(repo_id + " repository already exits")

def main(graphdb_url):
    '''
    Create cde repository in graph DB
    '''
    repo_id = "cde"
    repo_description = "Repository to store CDEs RDF documents"
    create_repository(graphdb_url, repo_id, repo_description)

    '''
    Create fdp repository in graph DB
    '''
    repo_id = "fdp"
    repo_description = "Repository to store FAIR Data Point's metadata RDF documents"
    create_repository(graphdb_url, repo_id, repo_description)


graphdb_url = sys.argv[1]
if graphdb_url.endswith("/"):
    graphdb_url = graphdb_url[:-1]
main(graphdb_url)

