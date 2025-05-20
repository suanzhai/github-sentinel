import asyncio
import os
from datetime import datetime

import schedule
import yaml

from core import fetcher, notifier, report, subscription

LOG_FILE = "logs/scheduler.log"

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {msg}\n")

async def run_scheduler_loop(interval: int):
    while True:
        schedule.run_pending()
        await asyncio.sleep(interval)

def job():
    repos = subscription.get_subscribed_repos()
    updates = fetcher.fetch_updates(repos)
    if updates:
        summary = report.generate(updates)
        notifier.send(summary)
        log("[Job] 更新发送完成")
    else:
        log("[Job] 无新更新")

def run():
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    schedule_cfg = config.get("schedule", {})
    schedule_type = schedule_cfg.get("type", "interval")
    if schedule_type == "interval":
        minutes = schedule_cfg.get("minutes", 60)
        log(f"[Scheduler] 每 {minutes} 分钟执行一次")
        schedule.every(minutes).minutes.do(job)
    elif schedule_type == "daily":
        schedule.every().day.at("09:00").do(job)
        log("[Scheduler] 每日 09:00 执行一次")
    elif schedule_type == "weekly":
        schedule.every().monday.at("09:00").do(job)
        log("[Scheduler] 每周一 09:00 执行一次")
    else:
        raise ValueError(f"不支持的调度类型: {schedule_type}")

    asyncio.run(run_scheduler_loop(60))
