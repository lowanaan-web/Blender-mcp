from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
from typing import Any

from blender_mcp.app import BlenderMCPApplication
from blender_mcp.transports import serve_http, serve_stdio


async def _health_tool(_payload: dict[str, Any]) -> dict[str, Any]:
    return {"status": "ok"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Blender MCP server")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to JSON config file. Env vars override file values.",
    )
    return parser


async def start(config_file: Path | None = None) -> None:
    app = BlenderMCPApplication.from_sources(config_file)
    app.tools.register("health", _health_tool)

    transport = app.config.server.transport
    if transport == "stdio":
        await app.run(serve_stdio)
    else:
        await app.run(serve_http)


def run() -> None:
    parser = build_parser()
    args = parser.parse_args()
    asyncio.run(start(args.config))


if __name__ == "__main__":
    run()
