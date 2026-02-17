from __future__ import annotations

import asyncio
import contextlib
import dataclasses
import json
import logging
import os
import signal
import time
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any


class ConfigError(ValueError):
    """Raised when configuration loading or validation fails."""


@dataclasses.dataclass(frozen=True, slots=True)
class ServerConfig:
    host: str
    port: int
    transport: str
    auth_token: str | None
    shutdown_timeout_seconds: float


@dataclasses.dataclass(frozen=True, slots=True)
class LoggingConfig:
    level: str
    service_name: str


@dataclasses.dataclass(frozen=True, slots=True)
class AppConfig:
    server: ServerConfig
    logging: LoggingConfig

    @classmethod
    def load(cls, config_file: Path | None = None) -> AppConfig:
        raw_config = cls._load_file(config_file)
        merged = cls._merge_env(raw_config)
        return cls._validate(merged)

    @staticmethod
    def _load_file(config_file: Path | None) -> dict[str, Any]:
        if config_file is None:
            default_path = os.environ.get("BLENDER_MCP_CONFIG", "")
            if not default_path:
                return {}
            config_file = Path(default_path)

        if not config_file.exists():
            raise ConfigError(f"Config file does not exist: {config_file}")

        suffix = config_file.suffix.lower()
        if suffix == ".json":
            return json.loads(config_file.read_text(encoding="utf-8"))
        if suffix in {".yaml", ".yml"}:
            raise ConfigError(
                "YAML config requires a parser dependency; use JSON for strict deployment"
            )

        raise ConfigError(
            "Unsupported config file format. Use JSON files and BLENDER_MCP_* env vars."
        )

    @staticmethod
    def _merge_env(config_data: dict[str, Any]) -> dict[str, Any]:
        data = json.loads(json.dumps(config_data))
        data.setdefault("server", {})
        data.setdefault("logging", {})

        env_map = {
            "BLENDER_MCP_HOST": ("server", "host"),
            "BLENDER_MCP_PORT": ("server", "port"),
            "BLENDER_MCP_TRANSPORT": ("server", "transport"),
            "BLENDER_MCP_AUTH_TOKEN": ("server", "auth_token"),
            "BLENDER_MCP_SHUTDOWN_TIMEOUT_SECONDS": (
                "server",
                "shutdown_timeout_seconds",
            ),
            "BLENDER_MCP_LOG_LEVEL": ("logging", "level"),
            "BLENDER_MCP_SERVICE_NAME": ("logging", "service_name"),
        }
        for env_name, (section, key) in env_map.items():
            value = os.environ.get(env_name)
            if value is None:
                continue
            data[section][key] = value
        return data

    @classmethod
    def _validate(cls, data: dict[str, Any]) -> AppConfig:
        server_data = data.get("server", {})
        logging_data = data.get("logging", {})

        host = cls._expect_str(server_data.get("host", "127.0.0.1"), "server.host")
        port = cls._expect_int(server_data.get("port", 8765), "server.port", 1, 65535)
        transport = cls._expect_str(
            server_data.get("transport", "stdio"), "server.transport"
        ).lower()
        if transport not in {"stdio", "http"}:
            raise ConfigError("server.transport must be one of: stdio, http")

        auth_token_value = server_data.get("auth_token", None)
        if auth_token_value in {"", None}:
            auth_token: str | None = None
        else:
            auth_token = cls._expect_str(auth_token_value, "server.auth_token")

        shutdown_timeout = cls._expect_float(
            server_data.get("shutdown_timeout_seconds", 15.0),
            "server.shutdown_timeout_seconds",
            min_value=0.1,
        )

        level = cls._expect_str(logging_data.get("level", "INFO"), "logging.level").upper()
        if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ConfigError(
                "logging.level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )
        service_name = cls._expect_str(
            logging_data.get("service_name", "blender-mcp"), "logging.service_name"
        )

        return AppConfig(
            server=ServerConfig(
                host=host,
                port=port,
                transport=transport,
                auth_token=auth_token,
                shutdown_timeout_seconds=shutdown_timeout,
            ),
            logging=LoggingConfig(level=level, service_name=service_name),
        )

    @staticmethod
    def _expect_str(value: Any, name: str) -> str:
        if not isinstance(value, str):
            raise ConfigError(f"{name} must be a string")
        return value

    @staticmethod
    def _expect_int(value: Any, name: str, min_value: int, max_value: int) -> int:
        try:
            parsed = int(value)
        except (TypeError, ValueError) as exc:
            raise ConfigError(f"{name} must be an integer") from exc
        if not min_value <= parsed <= max_value:
            raise ConfigError(f"{name} must be between {min_value} and {max_value}")
        return parsed

    @staticmethod
    def _expect_float(value: Any, name: str, min_value: float) -> float:
        try:
            parsed = float(value)
        except (TypeError, ValueError) as exc:
            raise ConfigError(f"{name} must be numeric") from exc
        if parsed < min_value:
            raise ConfigError(f"{name} must be >= {min_value}")
        return parsed


class JsonFormatter(logging.Formatter):
    def __init__(self, service_name: str):
        super().__init__()
        self._service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "service": self._service_name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "context"):
            payload["context"] = getattr(record, "context")
        return json.dumps(payload, separators=(",", ":"))


ToolCallable = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolCallable] = {}

    def register(self, name: str, handler: ToolCallable) -> None:
        if not name:
            raise ValueError("Tool name must not be empty")
        if name in self._tools:
            raise ValueError(f"Tool already registered: {name}")
        self._tools[name] = handler

    async def invoke(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        tool = self._tools.get(name)
        if tool is None:
            raise KeyError(f"Unknown tool: {name}")
        return await tool(payload)


class AuthMiddleware:
    def __init__(self, token: str | None):
        self._token = token

    def authorize(self, provided_token: str | None) -> bool:
        if self._token is None:
            return True
        return provided_token == self._token


class LifecycleHooks:
    def __init__(self) -> None:
        self._on_startup: list[Callable[[], Awaitable[None]]] = []
        self._on_shutdown: list[Callable[[], Awaitable[None]]] = []

    def add_startup(self, hook: Callable[[], Awaitable[None]]) -> None:
        self._on_startup.append(hook)

    def add_shutdown(self, hook: Callable[[], Awaitable[None]]) -> None:
        self._on_shutdown.append(hook)

    async def run_startup(self) -> None:
        for hook in self._on_startup:
            await hook()

    async def run_shutdown(self) -> None:
        for hook in reversed(self._on_shutdown):
            await hook()


class BlenderMCPApplication:
    def __init__(self, config: AppConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger
        self.tools = ToolRegistry()
        self.auth = AuthMiddleware(config.server.auth_token)
        self.lifecycle = LifecycleHooks()

        self._shutdown_event = asyncio.Event()
        self._inflight_tasks: set[asyncio.Task[Any]] = set()

    @classmethod
    def from_sources(cls, config_file: Path | None = None) -> BlenderMCPApplication:
        config = AppConfig.load(config_file)
        logger = cls._configure_logging(config.logging)
        app = cls(config=config, logger=logger)
        app._install_default_hooks()
        return app

    @staticmethod
    def _configure_logging(config: LoggingConfig) -> logging.Logger:
        root = logging.getLogger()
        root.handlers.clear()
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter(config.service_name))
        root.addHandler(handler)
        root.setLevel(getattr(logging, config.level))
        return logging.getLogger("blender_mcp")

    def _install_default_hooks(self) -> None:
        async def startup() -> None:
            self.logger.info("Application startup complete")

        async def shutdown() -> None:
            self.logger.info("Application shutdown complete")

        self.lifecycle.add_startup(startup)
        self.lifecycle.add_shutdown(shutdown)

    def request_shutdown(self) -> None:
        self._shutdown_event.set()

    async def wait_for_shutdown_signal(self) -> None:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            with contextlib.suppress(NotImplementedError):
                loop.add_signal_handler(sig, self.request_shutdown)
        await self._shutdown_event.wait()

    async def execute_tool_call(
        self,
        *,
        tool_name: str,
        payload: dict[str, Any],
        auth_token: str | None,
    ) -> dict[str, Any]:
        if not self.auth.authorize(auth_token):
            raise PermissionError("Unauthorized tool invocation")

        task = asyncio.create_task(self.tools.invoke(tool_name, payload))
        self._inflight_tasks.add(task)
        task.add_done_callback(self._inflight_tasks.discard)
        return await task

    async def drain_inflight(self) -> None:
        if not self._inflight_tasks:
            return

        self.logger.info(
            "Awaiting in-flight tool calls",
            extra={"context": {"count": len(self._inflight_tasks)}},
        )

        done, pending = await asyncio.wait(
            self._inflight_tasks,
            timeout=self.config.server.shutdown_timeout_seconds,
        )
        if pending:
            for task in pending:
                task.cancel()
            await asyncio.gather(*pending, return_exceptions=True)
            self.logger.warning(
                "Cancelled unresolved tool calls",
                extra={"context": {"cancelled_count": len(pending)}},
            )
        self.logger.info(
            "Tool call drain complete", extra={"context": {"completed": len(done)}}
        )

    async def run(self, serve: Callable[[BlenderMCPApplication], Awaitable[None]]) -> None:
        await self.lifecycle.run_startup()
        server_task = asyncio.create_task(serve(self))
        signal_task = asyncio.create_task(self.wait_for_shutdown_signal())

        done, pending = await asyncio.wait(
            {server_task, signal_task}, return_when=asyncio.FIRST_COMPLETED
        )

        if signal_task in done and not server_task.done():
            self.logger.info("Shutdown requested; stopping transport")
            server_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await server_task

        for task in pending:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

        await self.drain_inflight()
        await self.lifecycle.run_shutdown()
