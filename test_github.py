import streamlit as st
import requests

def test_github_issues():
    #token = os.getenv('GITHUB_TOKEN', '...')
    st.info(f"Get Token...", icon="ℹ️", width="stretch")
    token = st.secrets.tests.REPLICATE_API_TOKEN
    owner = "Me-creator-cpu"
    repo = "test_excel"
    
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": "open",
        }
    headers = {'Authorization': f'token {token}'}
    st.info(f"Send Request...", icon="ℹ️", width="stretch")
    r = requests.get(query_url, headers=headers, params=params)
    st.info(f"Got results...", icon="ℹ️", width="stretch")

    st.info(f"Send Request...", icon="ℹ️", width="stretch")
    query_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {}
    r = requests.get(query_url, headers=headers, params=params)
    st.info(f"Got results...", icon="ℹ️", width="stretch")
    
    result = r.json()
    st.write(r.json())
    return result
