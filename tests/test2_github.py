import streamlit as st
import requests
import pandas as pd
from pandas import json_normalize
import base64
import json
import datetime as gitDatetime
#https://elye-project.medium.com/3-easy-steps-to-programmatically-access-github-using-python-6d9dc8f1f7db
from pathlib import Path
from github import Auth
from github import Github

def write_data(sInfo, data):
    with st.expander(f'{sInfo}', expanded=False, icon=':material/table_view:', width='stretch'):
        data

github_token = st.secrets.tests.REPLICATE_API_TOKEN
usr_name = 'Me-creator-cpu'
repo_name = 'test_excel'
branch = 'main'

st.write(f"{github_token}")

auth = Auth.Token(github_token)  

# Create a GitHub object with your access token
g = Github(auth=auth)

# Get the repository object
repo = g.get_repo(f"{usr_name}/{repo_name}")

# Get all pull requests (adjust state and number parameters as needed)
pull_requests = repo.get_pulls(state="open", sort="created", direction="desc")

# Iterate through each pull request
for pull_request in pull_requests:
    # Initialize counters for added and deleted lines
    additions = 0
    deletions = 0

    # Get the pull request files
    files = pull_request.get_files()

    # Iterate through each file in the pull request
    for file in files:
        # Extract additions and deletions from the file object
        additions += file.additions
        deletions += file.deletions

    # Print information about the pull request with line counts
    st.write(f"** PR #{pull_request.number}: {pull_request.title} **")
    st.write(f"URL: {pull_request.html_url}")
    st.write(f"Added lines: {additions}")
    st.write(f"Deleted lines: {deletions}")
    st.write(f"Total lines changed: {additions + deletions}")

query_url = f"https://api.github.com/repos/{usr_name}/{repo_name}/commits"
params = {}
r = requests.get(query_url, headers=headers, params=params)
issues = g.search_issues(
            query=f'is:pr is:merged base:master repo:”{usr_name}/{repo_name}” created:>2026-03-01',
            sort='updated',
            order='desc'
            )

write_data('Issues',issues)

# Iterate through each issues to convert to pull requests
pull_requests = list()

for issue in issues:
    pull_requests.append(issue.as_pull_request())

write_data('Pull Requests',pull_requests)

