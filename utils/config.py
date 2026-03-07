import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "configs" / "config.json"

def load_config(path: str | None = None) -> dict:
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    with open(config_path, "r", encoding="utf-8-sig") as handle:
        cfg = json.load(handle)
        # Resolve API base URL, allowing override from environment
        base_api = f"{cfg['base_url'].rstrip('/')}/api"
        cfg["api_base_url"] = os.getenv(
            "API_BASE_URL", cfg.get("api_base_url") or base_api
        )

        # Resolve timeout, allow environment override via TIMEOUT_SECONDS
        cfg_timeout = cfg.get("timeout_seconds", 20)
        env_timeout = os.getenv("TIMEOUT_SECONDS")
        if env_timeout is not None:
            try:
                cfg["timeout_seconds"] = int(env_timeout)
            except (TypeError, ValueError):
                cfg["timeout_seconds"] = int(cfg_timeout)
        else:
            cfg["timeout_seconds"] = int(cfg_timeout)

        # Resolve headless flag, allow environment override via HEADLESS
        headless_env = os.getenv("HEADLESS")
        if headless_env is not None:
            cfg["headless"] = str(headless_env).lower() in {"1", "true", "yes", "y"}
        else:
            cfg["headless"] = bool(cfg.get("headless", True))
        return cfg

def get_admin_credentials(self):

    """获取管理员账号密码"""
    try:
        admin = self.config_data.get("admin", {})
        return {
            "account": admin.get("account"),
            "password": admin.get("password")
        }
    except:
        return {"account": None, "password": None}