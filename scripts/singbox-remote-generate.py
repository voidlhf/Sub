import json
import argparse
import os
import requests

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def download_json_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def extract_and_generate_new_outbounds(source_data):
    outbounds = source_data.get("outbounds", [])
    server_objects = [outbound for outbound in outbounds if "server" in outbound]
    server_tags = [outbound["tag"] for outbound in server_objects]
    new_objects = [
        {
            "tag": "select",
            "type": "selector",
            "default": "urltest",
            "outbounds": ["urltest"] + server_tags,
        },
        {"tag": "urltest", "type": "urltest", "outbounds": server_tags},
        {"tag": "chatgpt", "type": "selector", "outbounds": server_tags},
    ]
    direct_object = {"tag": "direct", "type": "direct"}
    server_objects.extend(new_objects)
    server_objects.append(direct_object)
    return server_objects


def replace_outbounds_in_fixed_target(source_data, output_file):
    target_file = "singbox-config/config.json"
    if not os.path.exists(target_file):
        raise FileNotFoundError(f"目标文件 '{target_file}' 未找到。")
    with open(target_file, "r", encoding="utf-8") as f:
        target_data = json.load(f)
    new_outbounds = extract_and_generate_new_outbounds(source_data)
    target_data["outbounds"] = new_outbounds

    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(target_data, f, indent=2, ensure_ascii=False)

    print(f"文件已保存到: {os.path.abspath(output_file)}")


def main():
    parser = argparse.ArgumentParser(description="处理 JSON 文件并替换 outbounds。")
    parser.add_argument("url", help="从指定 URL 下载源 JSON 文件（例如：1.json）")
    parser.add_argument("output", help="保存修改后数据的输出 JSON 文件")
    args = parser.parse_args()

    if not os.path.dirname(args.output):
        args.output = os.path.join(os.getcwd(), args.output)

    source_data = download_json_from_url(args.url)
    replace_outbounds_in_fixed_target(source_data, args.output)


if __name__ == "__main__":
    main()