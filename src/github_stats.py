import requests
import os

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ["ACCESS_TOKEN"]
USER_NAME = os.environ["USER_NAME"]

API_URL = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28"
}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

def get_user_profile(username):
    url = f"{API_URL}/users/{username}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_all_repos(username):
    repos = []
    page = 1
    per_page = 100
    while True:
        url = f"{API_URL}/users/{username}/repos?page={page}&per_page={per_page}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_star_count(repos):
    count = 0
    for repo in repos:
        count += repo["stargazers_count"]
    
    return count

def get_commit_count(username):
    query = f"author:{username}"
    url = f"{API_URL}/search/commits?q={query}"
    
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    
    data = response.json()
    
    return data.get("total_count", 0)