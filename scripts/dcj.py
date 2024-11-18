import os
import requests
import sys

# 将工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 定义下载 URL 和保存路径
url = "http://localhost:8090/sub?outFields=0&sub=https%3A%2F%2Fraw.githubusercontent.com%2Fdongchengjie%2Fairport%2Fmain%2Fsubs%2Fmerged%2Ftested_within.yaml"
save_path = "../singbox/dcj.json"

# 创建保存目录（如果目录不存在）
os.makedirs(os.path.dirname(save_path), exist_ok=True)

try:
    # 下载 JSON 文件
    response = requests.get(url)
    response.raise_for_status()  # 检查请求状态
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(response.text)
    print(f"下载完成，文件已保存至 {save_path}")


except requests.exceptions.RequestException as e:
    print(f"下载失败：{e}")
