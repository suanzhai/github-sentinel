import json

def get_subscribed_repos():
    with open("data/subscriptions.json", "r") as f:
        data = json.load(f)
    return data.get("repositories", [])
