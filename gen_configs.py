import os
import sys
import json
import argparse
import requests
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

API_BASE = "http://127.0.0.1:3000"
MIHOMO_DIR = "../mihomo"
SINGBOX_DIR = "../singbox"

def handle_one(name, url):
    print(f"处理订阅: {name}")

    local_url = f"{API_BASE}/download/sub?url={url}"
    mihomo_out = os.path.join(MIHOMO_DIR, f"{name}.yaml")
    singbox_out = os.path.join(SINGBOX_DIR, f"{name}.json")

    print("生成 Mihomo 配置...")
    subprocess.run(["python", "scripts/mihomo-remote-generate.py", local_url, mihomo_out])

    print("生成 Singbox 配置...")
    subprocess.run(["python", "scripts/singbox-remote-generate.py", local_url, singbox_out])

    print("-----------------------------")

def handle_json(json_input):
    if json_input.startswith("http://") or json_input.startswith("https://"):
        try:
            response = requests.get(json_input)
            response.raise_for_status()
            items = response.json()
        except Exception as e:
            print(f"下载 JSON 失败: {e}")
            return
    else:
        if not os.path.isfile(json_input):
            print("无效的 JSON 文件路径")
            return
        with open(json_input, "r", encoding="utf-8") as f:
            items = json.load(f)

    for item in items:
        name = item.get("name")
        url = item.get("url")
        if name and url:
            handle_one(name, url)
        else:
            print("跳过无效项：", item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成 Mihomo 和 Singbox 配置")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--json", help="JSON 文件路径或 URL（包含 name/url）")
    group.add_argument("--name", help="订阅名称（需配合 --url）")
    parser.add_argument("--url", help="订阅地址")

    args = parser.parse_args()

    if args.json:
        handle_json(args.json)
    elif args.name and args.url:
        handle_one(args.name, args.url)
    else:
        print("参数不完整，请使用 --json 或 --name 与 --url")