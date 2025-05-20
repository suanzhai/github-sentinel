import os

import yaml


def get_config():
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # 从环境变量读取 token
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        raise ValueError("❌ 未设置 GITHUB_TOKEN 环境变量，请先导出该变量。")

    config["github_token"] = github_token
    return config
