import requests

def test_github_issues():
    #token = os.getenv('GITHUB_TOKEN', '...')
    token = st.secrets.tests.REPLICATE_API_TOKEN
    owner = "Me-creator-cpu"
    repo = "test_excel"
    query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": "open",
        }
    headers = {'Authorization': f'token {token}'}
    r = requests.get(query_url, headers=headers, params=params)
    result = r.json()
    return result
