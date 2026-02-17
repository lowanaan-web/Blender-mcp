from __future__ import annotations

import asyncio
import json
from http import HTTPStatus
from typing import Any

from blender_mcp.app import BlenderMCPApplication


def _http_response(status: HTTPStatus, payload: dict[str, Any]) -> bytes:
    body = json.dumps(payload).encode("utf-8")
    headers = [
        f"HTTP/1.1 {status.value} {status.phrase}",
        "Content-Type: application/json",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "",
        "",
    ]
    return "\r\n".join(headers).encode("utf-8") + body


async def serve_http(app: BlenderMCPApplication) -> None:
    app.logger.info(
        "Starting http transport",
        extra={"context": {"host": app.config.server.host, "port": app.config.server.port}},
    )

    async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            head = await reader.readuntil(b"\r\n\r\n")
            request_line = head.splitlines()[0].decode("ascii", errors="ignore")
            method, path, _version = request_line.split(" ", 2)

            headers: dict[str, str] = {}
            for raw in head.decode("utf-8", errors="ignore").split("\r\n")[1:]:
                if not raw:
                    continue
                key, value = raw.split(":", 1)
                headers[key.lower().strip()] = value.strip()

            if method != "POST" or path != "/tool/invoke":
                writer.write(_http_response(HTTPStatus.NOT_FOUND, {"error": "Not Found"}))
                await writer.drain()
                return

            content_length = int(headers.get("content-length", "0"))
            if content_length <= 0:
                writer.write(
                    _http_response(
                        HTTPStatus.BAD_REQUEST, {"error": "Missing request body"}
                    )
                )
                await writer.drain()
                return

            body = await reader.readexactly(content_length)
            payload = json.loads(body)
            result = await app.execute_tool_call(
                tool_name=payload["tool"],
                payload=payload.get("payload", {}),
                auth_token=headers.get("authorization", "").replace("Bearer ", "")
                or None,
            )
            writer.write(_http_response(HTTPStatus.OK, {"result": result}))
            await writer.drain()
        except Exception as exc:  # runtime boundary
            writer.write(
                _http_response(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": str(exc)})
            )
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(
        handler,
        host=app.config.server.host,
        port=app.config.server.port,
    )

    async with server:
        await server.serve_forever()
