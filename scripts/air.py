import os
import requests
import sys

# 将工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 定义下载 URL 和保存路径
url = "http://127.0.0.1:8090/sub?outFields=0&sub=https%3A%2F%2Fyun-api.subcloud.xyz%2Fsub%3Ftarget%3Dclash%26url%3Dhttps%253A%252F%252Fsite.airapp.club%252Fapi%252Fv1%252Fclient%252Fmacsubscribe%253Ftoken%253D005ce824afc80b9fa9611fcace6d231a%26insert%3Dfalse%26config%3Dhttps%253A%252F%252Fraw.githubusercontent.com%252FACL4SSR%252FACL4SSR%252Fmaster%252FClash%252Fconfig%252FACL4SSR_Online.ini%26emoji%3Dtrue%26list%3Dfalse%26tfo%3Dfalse%26scv%3Dtrue%26fdn%3Dfalse%26sort%3Dfalse%26new_name%3Dtrue"
save_path = "../singbox/air.json"

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
