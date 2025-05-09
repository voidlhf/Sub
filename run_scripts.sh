#!/bin/bash

gen_configs_from_json() {
  local json_file="$1"
  local api_base="http://127.0.0.1:3000"
  local mihomo_dir="../mihomo"
  local singbox_dir="../singbox"

  if [[ -z "$json_file" || ! -f "$json_file" ]]; then
    echo "请提供有效的 JSON 文件路径"
    return 1
  fi

  jq -c '.[]' "$json_file" | while read -r item; do
    local name url response local_url mihomo_out singbox_out
    name=$(echo "$item" | jq -r '.name')
    url=$(echo "$item" | jq -r '.url')

    [[ -z "$name" || -z "$url" ]] && continue

    echo "正在添加订阅: $name"

    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$api_base/api/subs" \
      -H "Content-Type: application/json" \
      -d "{\"name\": \"$name\", \"url\": \"$url\"}")

    if [[ "$response" =~ ^20[01]$ ]]; then
      echo "订阅 [$name] 添加成功"

      local_url="$api_base/download/$name"
      mihomo_out="$mihomo_dir/$name.yaml"
      singbox_out="$singbox_dir/$name.json"

      echo "生成 Mihomo 配置..."
      python scripts/mihomo-remote-generate.py "$local_url" "$mihomo_out"

      echo "生成 Singbox 配置..."
      python scripts/singbox-remote-generate.py "$local_url" "$singbox_out"

      echo "清理订阅 [$name]..."
      curl -s -X DELETE "$api_base/api/sub/$name" > /dev/null
      echo "订阅 [$name] 已删除"
    else
      echo "订阅 [$name] 添加失败，状态码: $response"
    fi

    echo "-----------------------------"
  done
}

gen_configs_from_json "sub-zs.json"
gen_configs_from_json "sub.json"