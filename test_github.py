import streamlit as st
import requests
import pandas as pd
from pandas import json_normalize
#import json
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
    
    url_test = 'contents'    #OK, cf https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository--code-samples
    github_url = f'https://api.github.com/repos/{owner}/{repo}/{url_test}' 
    
    #github_url = f"https://api.github.com/user/starred/{owner}/{repo}"
    
    #query="q=language:py"
    #github_url = "https://api.github.com/search/repositories?q={query}" #{&page,per_page,sort,order}"
    
    result = requests.get(github_url, headers=headers, params=params)
    st.write(f'Testing: {url_test}')
    st.write(github_url)
    st.write(result)
    if result.status_code == 200:
        st.write(result.json())
    #st.write(token)
    #dataFrame = pd.read_json(result.json())
    
    dict = json.loads(result.json())
    df2 = json_normalize(dict[]) 
    df = pd.read_json(df2, orient='records')
    df
    return result
