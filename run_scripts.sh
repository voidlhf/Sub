#!/bin/bash

generate_mihomo() {
  local url=$1
  local output=$2
  python scripts/mihomo-remote-generate.py "$url" "$output"
}

generate_singbox() {
  local url=$1
  local output=$2
  local prefix="http://127.0.0.1:8080/sub?sub="
  python scripts/singbox-remote-generate.py "${prefix}${url}" "$output"
}

process_json() {
  local json_file=$1
  local output_dir=$2
  local mode=$3

  jq -c '.[]' "$json_file" | while read -r entry; do
    name=$(echo "$entry" | jq -r '.name')
    url=$(echo "$entry" | jq -r '.url')

    if [ "$mode" == "mihomo" ]; then
      generate_mihomo "$url" "$output_dir/$name.yaml"
    elif [ "$mode" == "singbox" ]; then
      generate_singbox "$url" "$output_dir/$name.json"
    fi
  done
}

python scripts/xf.py
process_json "sub-zs.json" "../mihomo" "mihomo"
process_json "sub.json" "../mihomo" "mihomo"
process_json "sub.json" "../singbox" "singbox"