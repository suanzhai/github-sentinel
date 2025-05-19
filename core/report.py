def generate(updates):
    report = "📌 GitHub Sentinel 报告\n\n"
    for repo, events in updates:
        report += f"🔹 **{repo}** 更新：\n"
        for e in events:
            report += f"- {e['type']} by {e['actor']['login']} at {e['created_at']}\n"
    return report
