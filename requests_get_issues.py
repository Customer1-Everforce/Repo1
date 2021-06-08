from github import Github
import requests
import os
from pprint import pprint

token = os.getenv('GITHUB_TOKEN', '5b80cd6dd28577ed249e762207a2d9831cf8c727')
repo = "API_test"
owner = "everforce-github"
query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
#query_url = f"https://api.github.com/repos/{repo}"
params = {
    "state": "open",
}
headers = {'Authorization': f'token {token}'}
r = requests.get(query_url, headers=headers, params=params)
pprint(r.json())


"""
token = os.getenv('GITHUB_TOKEN', '...')
owner = "MartinHeinz"
repo = "python-project-blueprint"
query_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
params = {
    "state": "open",
}
headers = {'Authorization': f'token {token}'}
r = requests.get(query_url, headers=headers, params=params)
pprint(r.json())
"""
