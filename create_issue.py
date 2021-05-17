from github import Github
import requests
import os
from pprint import pprint

token = os.getenv('GITHUB_TOKEN', '5b80cd6dd28577ed249e762207a2d9831cf8c727')
#repo = "API_test"
#repo = "everforce_editors"
owner = "everforce-github"

g = Github(token)
#repo = g.get_repo("{owner}/{repo}")
repo = g.get_repo("everforce-github/API_test")
#repo = g.get_repo("API_test/everforce-github")
i = repo.create_issue(
    title="Issue Title-s2",
    body="Text of the body.",
    #assignee="Gri_Vidi",
    labels=[
        repo.get_label("good first issue")
    ]
)
print("Issue created:\n",i)

"""
g = Github(token)
repo = g.get_repo("MartinHeinz/python-project-blueprint")
i = repo.create_issue(
    title="Issue Title",
    body="Text of the body.",
    assignee="MartinHeinz",
    labels=[
        repo.get_label("good first issue")
    ]
)
pprint(i)
"""
