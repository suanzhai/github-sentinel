import json
import threading

import typer

from core import fetcher, report, notifier, subscription

app = typer.Typer()

SUB_FILE = "data/subscriptions.json"

@app.command()
def list():
    """📋 显示当前订阅的 GitHub 仓库"""
    repos = subscription.get_subscribed_repos()
    typer.echo("当前订阅仓库：")
    for r in repos:
        typer.echo(f" - {r}")

@app.command()
def add(repo: str):
    """➕ 添加新的订阅仓库（格式：owner/repo）"""
    repos = subscription.get_subscribed_repos()
    if repo in repos:
        typer.echo("⚠️ 已订阅该仓库")
        return
    repos.append(repo)
    with open(SUB_FILE, "w") as f:
        json.dump({"repositories": repos}, f, indent=2)
    typer.echo(f"✅ 添加成功: {repo}")

@app.command()
def remove(repo: str):
    """❌ 移除订阅的仓库"""
    repos = subscription.get_subscribed_repos()
    if repo not in repos:
        typer.echo("⚠️ 未找到该仓库")
        return
    repos.remove(repo)
    with open(SUB_FILE, "w") as f:
        json.dump({"repositories": repos}, f, indent=2)
    typer.echo(f"🗑️ 已移除: {repo}")

@app.command()
def pull():
    """📡 立即拉取一次更新并生成报告"""
    repos = subscription.get_subscribed_repos()
    updates = fetcher.fetch_updates(repos)
    if updates:
        summary = report.generate(updates)
        notifier.send(summary)
        typer.echo("✅ 报告已发送")
    else:
        typer.echo("🔍 无更新内容")


@app.command()
def start():
    """🚀 启动定时调度器（异步后台运行）"""
    typer.echo("🔁 启动 GitHub Sentinel 异步调度任务...")

    def scheduler_runner():
        from core import scheduler
        scheduler.run()

    t = threading.Thread(target=scheduler_runner, daemon=True)
    t.start()

@app.command()
def interactive():
    """🧭 进入交互模式 CLI（使用英文命令）"""
    typer.echo("📡 欢迎使用 GitHub Sentinel 交互控制台")
    while True:
        typer.echo("\n可用命令：")
        typer.echo("  list    - 查看所有订阅")
        typer.echo("  add     - 添加新的订阅仓库")
        typer.echo("  remove  - 移除已订阅仓库")
        typer.echo("  pull    - 立即拉取更新并生成报告")
        typer.echo("  start   - 启动定时调度器")
        typer.echo("  exit    - 退出交互模式")

        command = typer.prompt("请输入命令").strip().lower()

        if command == "list":
            list()
        elif command == "add":
            repo = typer.prompt("请输入要订阅的仓库（格式：owner/repo）").strip()
            add(repo)
        elif command == "remove":
            repo = typer.prompt("请输入要移除的仓库（格式：owner/repo）").strip()
            remove(repo)
        elif command == "pull":
            pull()
        elif command == "start":
            start()
        elif command == "exit":
            typer.echo("👋 再见！")
            break
        else:
            typer.echo("❌ 未知命令，请重新输入。输入 help 查看帮助。")

