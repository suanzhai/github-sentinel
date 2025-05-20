import requests

from utils import config


class GitHubAPI:
    def __init__(self):
        self.token = config.get_config()["github_token"]
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_repo_events(self, repo_full_name):
        url = f"https://api.github.com/repos/{repo_full_name}/events"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
