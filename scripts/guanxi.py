import os
import re
import json
import requests
import sys

# 将工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 定义下载 URL 和保存路径
url = "http://127.0.0.1:8090/sub?outFields=0&sub=https%3A%2F%2Fwww.guanxi.cloudns.be%2Fapi%2Fv1%2Fclient%2Fsubscribe%2Ftoken%3D9e48312624d64c219f8e7u9af55b4k238bh5"
save_path = "../singbox/guanxi.json"

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
        if item.get("network") == "tcp":
            del item["network"]
    # 将 JSON 数据转换为字符串以执行替换操作
    data_str = json.dumps(data, ensure_ascii=False, indent=4)

    # 使用正则表达式替换所有 "-TG@MFJD666" 为空白字符串
    data_str = re.sub(r"-TG@MFJD666", "", data_str)
    data_str = re.sub(r"冠希公益", "公益节点", data_str)

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
