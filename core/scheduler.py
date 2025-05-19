import schedule
import time
from core import fetcher, notifier, report, subscription
import yaml

def run():
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    interval = config["schedule"]
    if interval == "daily":
        schedule.every().day.at("09:00").do(job)
    elif interval == "weekly":
        schedule.every().monday.at("09:00").do(job)

    print(f"[Scheduler] Running with interval: {interval}")
    while True:
        schedule.run_pending()
        time.sleep(60)

def job():
    repos = subscription.get_subscribed_repos()
    updates = fetcher.fetch_updates(repos)
    summary = report.generate(updates)
    notifier.send(summary)
