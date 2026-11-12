#!/usr/bin/env bash
set -euo pipefail

IMAGE="chunkflow:smoke"
CONTAINER="chunkflow-smoke"
PORT=$(python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)
MAX_WAIT=30

cleanup() {
  docker rm -f "$CONTAINER" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "==> Building image..."
docker build -t "$IMAGE" .

echo "==> Starting container..."
docker run -d --name "$CONTAINER" -p "$PORT:8001" "$IMAGE"

echo "==> Waiting for MCP server on :$PORT/mcp ..."
for _ in $(seq 1 "$MAX_WAIT"); do
  RESP=$(curl -sS --max-time 3 -X POST "http://localhost:$PORT/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"smoke-test","version":"0.0.1"}}}' \
    2>/dev/null || true)
  if echo "$RESP" | grep -q '"serverInfo"'; then
    echo "==> MCP initialize OK"
    echo "$RESP"
    exit 0
  fi
  sleep 1
done

echo "!! MCP server did not become ready on :$PORT/mcp" >&2
echo "---- container logs ----" >&2
docker logs "$CONTAINER" 2>&1 | tail -20 || true
exit 1
