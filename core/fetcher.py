import json
import os

from utils.github_api import GitHubAPI


def fetch_updates(repos):
    api = GitHubAPI()
    updates = []
    for repo in repos:
        new_events = api.get_repo_events(repo)
        cached_path = f"data/cache/{repo.replace('/', '_')}.json"
        old_events = []
        if os.path.exists(cached_path):
            with open(cached_path, "r") as f:
                old_events = json.load(f)
        diff = [e for e in new_events if e not in old_events]
        if diff:
            updates.append((repo, diff))
            with open(cached_path, "w") as f:
                json.dump(new_events, f, indent=2)
    return updates
