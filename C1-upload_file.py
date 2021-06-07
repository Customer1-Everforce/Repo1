from github import Github
import requests
import os
from pprint import pprint
import base64
import urllib
import http

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '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')
REPO = "API_test"
OWNER = "Customer1-Everforce"
BRANCH="update-dependencies"
FILENAME="C1-POSTed-file.txt"
SHA=BRANCH
AUTHOR = "Ms.USA"
AUTHOR_EMAIL = "Ms.USA@email.com"


def github_request(method, url, headers=None, data=None, params=None):
    """Execute a request to the GitHUB API, handling redirect"""
    if not headers:
        headers = {}
    headers.update({
        "User-Agent": "Agent 007",
        "Authorization": "Bearer " + GITHUB_TOKEN,
    })

    url_parsed = urllib.parse.urlparse(url)
    url_path = url_parsed.path
    if params:
        url_path += "?" + urllib.parse.urlencode(params)

    data = data and json.dumps(data)

    conn.request(method, url_path, body=data, headers=headers)
    response = conn.getresponse()
    if response.status == 302:
        return github_request(method, response.headers["Location"])

    if response.status >= 400:
        headers.pop('Authorization', None)
        raise Exception(
            f"Error: {response.status} - {json.loads(response.read())} - {method} - {url} - {data} - {headers}"
        )

    return (response, json.loads(response.read().decode()))

def upload_to_github(repository, src, dst, author_name, author_email, git_message, branch=BRANCH):
    # Get last commit SHA of a branch
    resp, jeez = github_request("GET", f"/repos/{repository}/git/ref/{branch}")
    last_commit_sha = jeez["object"]["sha"]
    print("Last commit SHA: " + last_commit_sha)

    base64content = base64.b64encode(open(src, "rb").read())
    resp, jeez = github_request(
        "POST",
        f"/repos/{repository}/git/blobs",
        data={
            "content": base64content.decode(),
            "encoding": "base64"
        },
    )
    blob_content_sha = jeez["sha"]

    resp, jeez = github_request(
        "POST",
        f"/repos/{repository}/git/trees",
        data={
            "base_tree":
            last_commit_sha,
            "tree": [{
                "path": dst,
                "mode": "100644",
                "type": "blob",
                "sha": blob_content_sha,
            }],
        },
    )
    tree_sha = jeez["sha"]

    resp, jeez = github_request(
        "POST",
        f"/repos/{repository}/git/commits",
        data={
            "message": git_message,
            "author": {
                "name": author_name,
                "email": author_email,
            },
            "parents": [last_commit_sha],
            "tree": tree_sha,
        },
    )
    new_commit_sha = jeez["sha"]

    resp, jeez = github_request(
        "PATCH",
        f"/repos/{repository}/git/refs/{branch}",
        data={"sha": new_commit_sha},
    )
    return (resp, jeez)

upload_to_github(REPO,FILENAME, FILENAME, AUTHOR, AUTHOR_EMAIL, "POSTed file using API", BRANCH)

#https://stackoverflow.com/questions/11801983/how-to-create-a-commit-and-push-into-repo-with-github-api-v3
