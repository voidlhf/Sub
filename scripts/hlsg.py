import os
import requests
import sys

# 将工作目录切换到脚本所在的目录
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# 定义基础 URL 和拼接参数
base_url = "https://clash2sfa.xmdhs.com/sub"
config_url = "https://raw.githubusercontent.com/voidlhf/Sub/refs/heads/branch1/config.json"
sub_url = "https://ovo.o00o.ooo/ooo"

# 拼接完整的 URL
url = f"{base_url}?configurl={config_url}&outFields=0&sub={sub_url}"

save_path = "../singbox/hlsg.json"

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
