import requests
import yaml

def send(message):
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
    if config["notifier"]["type"] == "slack":
        webhook = config["notifier"]["webhook_url"]
        requests.post(webhook, json={"text": message})
