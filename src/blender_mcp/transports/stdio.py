from __future__ import annotations

import asyncio
import json
import sys
from typing import Any

from blender_mcp.app import BlenderMCPApplication


async def serve_stdio(app: BlenderMCPApplication) -> None:
    loop = asyncio.get_running_loop()
    app.logger.info("Starting stdio transport")

    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if line == "":
            app.logger.info("Stdio stream closed")
            app.request_shutdown()
            return

        line = line.strip()
        if not line:
            continue

        message: dict[str, Any] | None = None
        try:
            message = json.loads(line)
            request_id = message["id"]
            tool_name = message["tool"]
            payload = message.get("payload", {})
            auth_token = message.get("auth_token")
            result = await app.execute_tool_call(
                tool_name=tool_name,
                payload=payload,
                auth_token=auth_token,
            )
            response: dict[str, Any] = {"id": request_id, "result": result}
        except Exception as exc:  # runtime boundary
            response = {
                "id": message.get("id") if isinstance(message, dict) else None,
                "error": str(exc),
            }

        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
