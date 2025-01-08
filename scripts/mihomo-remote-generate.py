import requests
import os
import sys
import argparse
import re
import ruamel.yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString


script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)


def download_yaml(url):
    headers = {"User-Agent": "clash.meta"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def preprocess_yaml(yaml_content):
    content = re.sub(r"!\<str\>", "", yaml_content)
    return content


def extract_proxies(yaml_content):
    yaml_content = preprocess_yaml(yaml_content)
    yaml = ruamel.yaml.YAML(typ="rt")
    data = yaml.load(yaml_content)
    return data.get("proxies", [])


def load_config(config_path):
    yaml = ruamel.yaml.YAML(typ="rt")
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.load(file)


def insert_proxies_to_config(config_data, proxies):
    proxy_groups_index = None
    for idx, key in enumerate(config_data.keys()):
        if key == "proxy-groups":
            proxy_groups_index = idx
            break

    if proxy_groups_index is not None:
        items = list(config_data.items())
        items.insert(proxy_groups_index, ("proxies", proxies))
        config_data.clear()
        config_data.update(dict(items))
    else:
        config_data["proxies"] = proxies
    return config_data


def insert_names_into_proxy_groups(config_data):
    proxies = config_data.get("proxies", [])
    proxy_groups = config_data.get("proxy-groups", [])

    proxy_names = [proxy.get("name") for proxy in proxies if "name" in proxy]
    excluded_names = ["🎯 全球直连", "🛑 全球拦截", "🍃 应用净化"]

    for group in proxy_groups:
        if "proxies" in group:
            if group.get("name") not in excluded_names:
                if not group["proxies"]:
                    group["proxies"] = proxy_names
                else:
                    group["proxies"].extend(proxy_names)

    return config_data


def apply_quotes_to_strings(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = apply_quotes_to_strings(value)
    elif isinstance(data, list):
        return [apply_quotes_to_strings(item) for item in data]
    elif isinstance(data, str):
        return DoubleQuotedScalarString(data)
    return data


def save_result(config_data, result_path):
    dir_name = os.path.dirname(result_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    yaml = ruamel.yaml.YAML(typ="rt")
    yaml.width = float("inf")
    config_data = apply_quotes_to_strings(config_data)
    with open(result_path, "w", encoding="utf-8") as file:
        yaml.dump(config_data, file)


def main(url, result_path):
    yaml_content = download_yaml(url)
    proxies = extract_proxies(yaml_content)

    config_path = os.path.join("mihomo-config", "config.yaml")
    config_data = load_config(config_path)

    updated_config = insert_proxies_to_config(config_data, proxies)
    updated_config = insert_names_into_proxy_groups(updated_config)

    save_result(updated_config, result_path)
    print(f"处理完成，结果已保存到 {result_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="通过URL下载YAML文件并更新config.yaml")
    parser.add_argument("url", help="需要下载的YAML文件URL")
    parser.add_argument("result_path", help="保存结果的路径")
    args = parser.parse_args()

    main(args.url, args.result_path)