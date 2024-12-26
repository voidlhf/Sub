import os
import yaml
import requests
import argparse

def download_file(url, save_path):
    headers = {
        "User-Agent": "clash.meta"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if not save_path:
        raise ValueError("保存路径无效，请提供有效的文件路径")

    save_dir = os.path.dirname(save_path) if os.path.dirname(save_path) else os.getcwd()
    os.makedirs(save_dir, exist_ok=True)

    with open(save_path, "wb") as file:
        file.write(response.content)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    parser = argparse.ArgumentParser(description="通过 URL 下载 YAML 文件并合并内容")
    parser.add_argument("url", help="config.yaml 文件的 URL")
    parser.add_argument("config_path", help="保存的 config.yaml 文件路径")
    args = parser.parse_args()

    file_url = args.url
    config_path = args.config_path

    general_path = os.path.join(script_dir, "config/general.yaml")
    proxy_groups_path = os.path.join(script_dir, "config/proxy-groups.yaml")
    rules_path = os.path.join(script_dir, "config/rules.yaml")

    if not config_path:
        print("提供的 config.yaml 文件路径无效。")
        return

    download_file(file_url, config_path)

    with open(config_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    with open(general_path, "r", encoding="utf-8") as file:
        general_data = yaml.safe_load(file)

    with open(proxy_groups_path, "r", encoding="utf-8") as file:
        proxy_groups_data = yaml.safe_load(file)

    with open(rules_path, "r", encoding="utf-8") as file:
        rules_data = yaml.safe_load(file)

    proxies_data = data.get("proxies", [])
    proxy_names = [proxy.get("name") for proxy in proxies_data if "name" in proxy]

    combined_data = {}
    combined_data.update(general_data)
    combined_data["proxies"] = proxies_data

    proxy_groups = proxy_groups_data.get("proxy-groups", [])
    excluded_names = {"🛑 全球拦截", "🍃 应用净化", "🎯 全球直连"}

    for group in proxy_groups:
        if group.get("name") in excluded_names:
            continue
        if "proxies" not in group or group["proxies"] is None:
            group["proxies"] = []
        group["proxies"].extend(proxy_names)

    combined_data["proxy-groups"] = proxy_groups

    if isinstance(rules_data, dict):
        if "rules" in rules_data:
            combined_data["rules"] = rules_data["rules"]
    else:
        raise ValueError("rules.yaml 的格式应为字典类型，且包含 rules 键")

    os.makedirs(os.path.dirname(config_path) if os.path.dirname(config_path) else os.getcwd(), exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as file:
        yaml.dump(
            combined_data,
            file,
            allow_unicode=True,
            default_flow_style=False,
            indent=2,
            sort_keys=False
        )

    print(f"文件已覆盖，内容已合并到 {config_path}。")

if __name__ == "__main__":
    main()