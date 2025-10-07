#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://127.0.0.1:3000"

echo "[Health] waiting for sandbox service at ${BASE_URL} ..."
for i in {1..30}; do
  if curl -sS "${BASE_URL}/" >/dev/null; then
    echo "[Health] service is up"
    break
  fi
  sleep 1
  if [[ $i -eq 30 ]]; then
    echo "[Health] service not available after 30s" >&2
    exit 1
  fi
done

make_req() {
  local label="$1"
  local payload_file="$2"
  echo "\n[${label}] request body:" && cat "${payload_file}" && echo
  echo "[${label}] response:"
  curl -sS -X POST "${BASE_URL}/sandbox/python" \
    -H 'Content-Type: application/json' \
    --data-binary @"${payload_file}" \
    | python3 -m json.tool || true
}

# Test 1: simple variable result
cat >/tmp/p1.json <<'JSON'
{
  "code": "result = 42",
  "variables": {}
}
JSON
make_req "TEST 1: result = 42" /tmp/p1.json

# Test 2: front-end template main(data1, data2) (auto-call with variables)
cat >/tmp/p2.json <<'JSON'
{
  "code": "def main(data1, data2):\n    return { \"result\": data1, \"data2\": data2 }",
  "variables": { "data1": 5, "data2": 10 }
}
JSON
make_req "TEST 2: main(data1, data2) with variables" /tmp/p2.json

# Test 3: matplotlib image with Chinese labels (returns base64)
cat >/tmp/p3.json <<'JSON'
{
  "code": "import matplotlib.pyplot as plt\n# 示例数据\nx = [1, 2, 3, 4, 5]\ny = [10, 12, 15, 14, 16]\n# 绘制折线图\nplt.plot(x, y)\n# 添加标题和标签\nplt.title(\"折线图示例\")\nplt.xlabel(\"X轴标签\")\nplt.ylabel(\"Y轴标签\")\nplt.show()",
  "variables": {}
}
JSON
make_req "TEST 3: matplotlib base64 image" /tmp/p3.json

# Test 4: dangerous import should be blocked
cat >/tmp/p4.json <<'JSON'
{
  "code": "import os\nresult = os.getcwd()",
  "variables": {}
}
JSON
make_req "TEST 4: dangerous import (expect error)" /tmp/p4.json

echo "\n[Done] local sandbox tests completed"