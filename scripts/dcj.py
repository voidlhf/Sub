import os
import requests
import sys
import json  # 用于格式化 JSON

# 将工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 定义基础 URL 和拼接参数
base_url = "https://clash2sfa.xmdhs.com/sub"
config_url = "https://raw.githubusercontent.com/voidlhf/Sub/refs/heads/branch1/config.json"
sub_url = "https://raw.githubusercontent.com/dongchengjie/airport/main/subs/merged/tested_within.yaml"

# 拼接完整的 URL
url = f"{base_url}?configurl={config_url}&outFields=0&sub={sub_url}"

save_path = "../singbox/dcj.json"

# 创建保存目录（如果目录不存在）
os.makedirs(os.path.dirname(save_path), exist_ok=True)

try:
    # 下载 JSON 文件
    response = requests.get(url)
    response.raise_for_status()  # 检查请求状态

    # 尝试解析为 JSON 并格式化
    try:
        json_data = response.json()  # 将响应内容解析为 JSON
        formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)  # 格式化 JSON
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}")
        sys.exit(1)

    # 保存格式化后的 JSON 文件
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(formatted_json)
    print(f"下载完成，文件已保存至 {save_path}")

except requests.exceptions.RequestException as e:
    print(f"下载失败：{e}")