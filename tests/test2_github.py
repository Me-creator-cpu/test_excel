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

def upload_to_github(github_token: str,
                     source_file: str, destination_folder: str,
                     github_repo: str, git_branch: str) -> None:
    """
    Uploads a file to a GitHub Pages repository using the PyGithub library.
    Parameters:
        github_token: Github token for authentication
        source_file: The path of the local file to be uploaded
        destination_folder: The path of the folder in the GitHub repository where the file will be uploaded
        github_repo: The name of the GitHub repository
        git_branch: The name of the branch in the GitHub repository
    """
    #from github import Github

    # Create a Github instance using token
    g = Github(github_token)
    # Get the repository object
    #repo = g.get_user().get_repo(github_repo)
    repo = g.get_repo(github_repo)
    # Get the branch object
    branch = repo.get_branch(git_branch)
    # Create the path of the file in the GitHub repository
    path = destination_folder + "/" + source_file.split("/")[-1]
    # Create or update the file in the GitHub repository
    try:
        # Get the existing file details if it exists
        existing_file = repo.get_contents(path, ref=branch.name)
        # Update the file
        repo.update_file(path, "Update file", open(source_file, 'rb').read(), existing_file.sha,
                         branch=branch.name)
        st.write(f"File '{path}' updated successfully.")
    except Exception as e:
        # If the file does not exist, create it
        #repo.create_file(path, "Upload file", open(source_file, 'rb').read(), branch=branch.name)
        source_file_test='test_api.txt'
        test_sha='30d74d258442c7c65512eafab474568dd706c430'
        repo.create_file(path, "Upload file", open(source_file_test, 'rb').read(), branch=branch.name,sha=test_sha)
        st.write(f"File '{path}' created successfully.")

#github_token = st.secrets.tests.REPLICATE_API_TOKEN
github_token = st.secrets.tests.CLASSIC_TOKEN
usr_name = 'Me-creator-cpu'
repo_name = 'test_excel'
branch = 'main'

sha='30d74d258442c7c65512eafab474568dd706c430'
test_filename='test_api.txt'

st.write(f"{github_token}")

auth = Auth.Token(github_token)  

# Create a GitHub object with your access token
g = Github(auth=auth)

# Get the repository object
repo = g.get_repo(f"{usr_name}/{repo_name}")

contents = repo.get_contents(test_filename)
st.write(contents)

#ContentFile, Commit=repo.create_file("test.txt", "test", "test", branch=branch)
upload_to_github(github_token=github_token,
                 source_file='test_api_2.txt',
                 destination_folder='',
                 github_repo=f"{usr_name}/{repo_name}",
                 git_branch=branch)

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

query_url = f'https://api.github.com/repos/{usr_name}/{repo_name}/issues'
params = {
    'state': 'open',
    }
headers = {'Authorization': f'token {github_token}'}
r = requests.get(query_url, headers=headers, params=params)

issues = g.search_issues(
            query=f'is:pull-request repo:”{usr_name}/{repo_name}”',
            #sort='updated',
            order='desc'
            )

write_data('Issues',issues)

# Iterate through each issues to convert to pull requests
pull_requests = list()

for issue in issues:
    pull_requests.append(issue.as_pull_request())

write_data('Pull Requests',pull_requests)

st.write('Closing connextion...')
g.close()