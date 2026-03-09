import streamlit as st
import requests
import pandas as pd
from pandas import json_normalize
import base64
import json
import datetime as gitDatetime
#import pygit2

def test_github_issues():
    #token = os.getenv('GITHUB_TOKEN', '...')
    st.info(f"Get Token...", icon="ℹ️", width="stretch")
    token = st.secrets.tests.REPLICATE_API_TOKEN
    owner = 'Me-creator-cpu'
    repo = 'test_excel'
    branch = 'main'
    url_test = 'hooks'
    
    query_url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    params = {
        'state': 'open',
        }
    headers = {'Authorization': f'token {token}'}
    st.info(f"Send Request...", icon="ℹ️", width="stretch")
    r = requests.get(query_url, headers=headers, params=params)
    st.info(f"Got results...", icon="ℹ️", width="stretch")

    if 1 == 2:
        st.info(f"Send Request...", icon="ℹ️", width="stretch")
        query_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {}
        r = requests.get(query_url, headers=headers, params=params)
        st.info(f"Got results...", icon="ℹ️", width="stretch")
        
        result = r.json()
        st.write('List commits')
        st.write(r.json())

    #https://docs.github.com/en/rest/meta/meta?apiVersion=2022-11-28#get-all-api-versions
    #github_url = 'https://github.com/USERNAME/REPOSITORY/tree/master/FOLDER'  # change USERNAME, REPOSITORY and FOLDER with actual name

    url_test = 'languages'    #OK
    
    url_test = 'contents/data'    #OK, cf https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository--code-samples
    github_url = f'https://api.github.com/repos/{owner}/{repo}/{url_test}' 
    
    #github_url = f"https://api.github.com/user/starred/{owner}/{repo}"
    
    #query="q=language:py"
    #github_url = "https://api.github.com/search/repositories?q={query}" #{&page,per_page,sort,order}"
    
    result = requests.get(github_url, headers=headers, params=params)
    st.write(f'Testing: {url_test}')
    st.write(github_url)
    st.write(result)
    #if result.status_code == 200:
    #    st.write(result.json())
    str_json=result.json()
    st.write(pd.json_normalize(str_json))

    st.write(f'Testing branch: {branch}')
    github_url = f'https://api.github.com/repos/{owner}/{repo}/branches/{branch}' 
    result = requests.get(github_url, headers=headers, params=params)
    if result.status_code == 200:
        str_json=result.json()
        str_json
        str_json["_links"]["html"]
    
    #https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#create-or-update-file-contents--code-samples
    fileName='todo.txt'
    url_test = f'contents/data/{fileName}'
    github_url = f'https://api.github.com/repos/{owner}/{repo}/{url_test}' 
    push_to_repo_branch(
        gitHubFileName=github_url,
        fileName=fileName,
        repo_slug=f'{owner}/{repo}',
        branch=branch,
        user=owner,
        token=st.secrets.tests.REPLICATE_API_TOKEN,
        )
    return result

def push_to_repo_branch(gitHubFileName, fileName, repo_slug, branch, user, token):
    '''
    Push file update to GitHub repo
    
    :param gitHubFileName: the name of the file in the repo
    :param fileName: the name of the file on the local branch
    :param repo_slug: the github repo slug, i.e. username/repo
    :param branch: the name of the branch to push the file to
    :param user: github username
    :param token: github user token
    :return None
    :raises Exception: if file with the specified name cannot be found in the repo
    '''
    
    message = "Automated update " + str(gitDatetime.datetime.now())
    path = "https://api.github.com/repos/%s/branches/%s" % (repo_slug, branch)
    path = f"https://api.github.com/repos/{repo_slug}/branches/{branch}/data"
    

    r = requests.get(path, auth=(user,token))
    if not r.ok:
        st.write("Error when retrieving branch info from %s" % path)
        st.write("Reason: %s [%d]" % (r.text, r.status_code))
        raise
    rjson = r.json()
    treeurl = rjson['commit']['commit']['tree']['url']
    r2 = requests.get(treeurl, auth=(user,token))
    if not r2.ok:
        st.write("Error when retrieving commit tree from %s" % treeurl)
        st.write("Reason: %s [%d]" % (r2.text, r2.status_code))
        raise
    r2json = r2.json()
    sha = None
    st.write('r2json')
    st.write(r2json)
    for file in r2json['tree']:
        # Found file, get the sha code
        st.write(file['path'])
        if file['path'] == gitHubFileName:
            sha = file['sha']

    # if sha is None after the for loop, we did not find the file name!
    if sha is None:
        st.write(f"Could not find {gitHubFileName} in repos {repo_slug}")
        raise Exception

    with open(fileName) as data:
        content = base64.b64encode(data.read())

    # gathered all the data, now let's push
    inputdata = {}
    inputdata["path"] = gitHubFileName
    inputdata["branch"] = branch
    inputdata["message"] = message
    inputdata["content"] = content
    if sha:
        inputdata["sha"] = str(sha)

    updateURL = f"https://api.github.com/repos/{repo_slug}/contents/" + gitHubFileName
    updateURL = gitHubFileName
    try:
        rPut = requests.put(updateURL, auth=(user,token), data = json.dumps(inputdata))
        if not rPut.ok:
            st.write("Error when pushing to %s" % updateURL)
            st.write("Reason: %s [%d]" % (rPut.text, rPut.status_code))
            raise Exception
    except requests.exceptions.RequestException as e:
        st.write('Something went wrong! I will print all the information that is available so you can figure out what happend!')
        st.write(rPut)
        st.write(rPut.headers)
        st.write(rPut.text)
        st.write(e)

