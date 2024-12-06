import os
import re
import json
import requests
import sys

# 将工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 定义基础 URL 和拼接参数
base_url = "https://clash2sfa.xmdhs.com/sub"
config_url = "https://raw.githubusercontent.com/voidlhf/Sub/refs/heads/branch1/config.json"
sub_url = "https://sublinks.52cloud.eu.org/api/v1/client/subscribe?token=b26fe554f300d7c9573d858c11b50a0b"

# 拼接完整的 URL
url = f"{base_url}?configurl={config_url}&outFields=0&sub={sub_url}"

save_path = "../singbox/bzy.json"

# 创建保存目录（如果目录不存在）
os.makedirs(os.path.dirname(save_path), exist_ok=True)

try:
    # 下载 JSON 文件
    response = requests.get(url)
    response.raise_for_status()  # 检查请求状态
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"下载完成，文件已保存至 {save_path}")

    # 读取 JSON 文件
    with open(save_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 在 JSON 数据中添加 udp_over_tcp 字段
    for item in data.get("outbounds", []):
        if item.get("method") == "chacha20-ietf-poly1305":
            item["udp_over_tcp"] = {"enabled": True, "version": 2}

    # 将 JSON 数据转换为字符串以执行替换操作
    data_str = json.dumps(data, ensure_ascii=False, indent=4)

    # 使用正则表达式替换所有 "-TG@MFJD666" 为空白字符串
    data_str = re.sub(r" @mfbpn", "", data_str)

    # 将替换后的字符串解析回 JSON 对象
    data = json.loads(data_str)

    # 将修改后的 JSON 数据保存回文件
    with open(save_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("数据处理完成")

except requests.exceptions.RequestException as e:
    print(f"下载失败：{e}")
except json.JSONDecodeError as e:
    print(f"解析 JSON 文件失败：{e}")
