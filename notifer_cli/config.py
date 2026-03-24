"""Configuration management for Notifer CLI."""
import os
from pathlib import Path
from typing import Optional, Any
import yaml


class Config:
    """Configuration for Notifer CLI."""

    # Default production server - hardcoded, no configuration needed
    DEFAULT_SERVER = "https://app.notifer.io"

    def __init__(self):
        """Initialize config with defaults."""
        self.server: str = self.DEFAULT_SERVER
        self.api_key: Optional[str] = None
        self.defaults: dict[str, Any] = {
            "priority": 3,
            "tags": [],
        }

    @classmethod
    def config_path(cls) -> Path:
        """Get config file path."""
        return Path.home() / ".notifer.yaml"

    @classmethod
    def load(cls) -> "Config":
        """Load config from file."""
        config = cls()
        config_file = cls.config_path()

        if config_file.exists():
            with open(config_file, "r") as f:
                data = yaml.safe_load(f) or {}

            config.server = data.get("server", config.server)
            config.api_key = data.get("api_key")
            config.defaults = data.get("defaults", config.defaults)

        return config

    def save(self):
        """Save config to file."""
        config_file = self.config_path()
        data = {}

        # Only save server if it differs from default
        if self.server != self.DEFAULT_SERVER:
            data["server"] = self.server

        if self.api_key:
            data["api_key"] = self.api_key

        data["defaults"] = self.defaults

        with open(config_file, "w") as f:
            yaml.safe_dump(data, f, default_flow_style=False)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dict."""
        return {
            "server": self.server,
            "api_key": self.api_key or "(not set)",
            "defaults": self.defaults,
        }
