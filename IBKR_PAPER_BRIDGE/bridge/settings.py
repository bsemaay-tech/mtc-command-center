"""pydantic-settings for Crypto Paper Bridge.

Env vars are optional at import time; missing keys disable the related feature:
  HL_ACCOUNT_ADDRESS: Hyperliquid account address (main wallet)
  HL_API_WALLET_KEY: Hyperliquid agent/API wallet private key
  ANTHROPIC_API_KEY: Anthropic API key (Claude veto)
  XAI_API_KEY: xAI API key (Grok regime)
  HL_LIVE_ACK: must be I_UNDERSTAND_THIS_IS_REAL_MONEY for mainnet
  TELEGRAM_BOT_TOKEN: Telegram bot token (optional)
  TELEGRAM_CHAT_ID: Telegram chat ID (optional)
"""

from __future__ import annotations

import os
import string
from typing import Tuple

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables with safe defaults."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    hl_account_address: str = ""
    hl_api_wallet_key: str = ""
    hl_live_ack: str = ""
    anthropic_api_key: str = ""
    xai_api_key: str = ""
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""


settings = Settings()

# ---------------------------------------------------------------------------
# import-safe non-Windows winreg guard
# ---------------------------------------------------------------------------
try:
    import winreg

    _HAS_WINREG = True
except ImportError:
    winreg = None  # type: ignore[assignment]
    _HAS_WINREG = False


# ---------------------------------------------------------------------------
# reusable Hyperliquid credential resolver
# ---------------------------------------------------------------------------


def _is_valid_hex_address(value: str) -> bool:
    """Return True if *value* is a 0x-prefixed 40-hex (20-byte) address."""
    if not value.startswith("0x"):
        return False
    body = value[2:]
    return len(body) == 40 and all(c in string.hexdigits for c in body)


def _is_valid_hex_key(value: str) -> bool:
    """Return True if *value* is an optional-0x 64-hex (32-byte) private key."""
    body = value[2:] if value.startswith("0x") else value
    return len(body) == 64 and all(c in string.hexdigits for c in body)


def resolve_hyperliquid_credentials() -> Tuple[str, str, str]:
    """Return ``(account_address, api_wallet_key, source)``.

    *source* is exactly ``"process_env"`` or ``"user_registry"``.

    Resolution order:

    1. *both* ``HL_ACCOUNT_ADDRESS`` and ``HL_API_WALLET_KEY`` from
       ``os.environ`` (whitespace-stripped) pass format validation.
    2. *both* values read from
       ``HKEY_CURRENT_USER\\Environment`` pass the same validation.
    3. Raise ``RuntimeError`` whose message contains **no credential
       material**.
    """
    # -- 1. process env --------------------------------------------------
    env_account = os.environ.get("HL_ACCOUNT_ADDRESS", "").strip()
    env_key = os.environ.get("HL_API_WALLET_KEY", "").strip()
    if _is_valid_hex_address(env_account) and _is_valid_hex_key(env_key):
        return env_account, env_key, "process_env"

    # -- 2. user registry ------------------------------------------------
    if _HAS_WINREG:
        try:
            with winreg.OpenKey(  # type: ignore[attr-defined]
                winreg.HKEY_CURRENT_USER, "Environment"
            ) as reg_key:
                reg_account, _ = winreg.QueryValueEx(  # type: ignore[attr-defined]
                    reg_key, "HL_ACCOUNT_ADDRESS"
                )
                reg_key_val, _ = winreg.QueryValueEx(  # type: ignore[attr-defined]
                    reg_key, "HL_API_WALLET_KEY"
                )
            reg_account = reg_account.strip() if isinstance(reg_account, str) else ""
            reg_key_val = reg_key_val.strip() if isinstance(reg_key_val, str) else ""
            if _is_valid_hex_address(reg_account) and _is_valid_hex_key(reg_key_val):
                return reg_account, reg_key_val, "user_registry"
        except Exception:
            pass

    # -- 3. no valid source ----------------------------------------------
    raise RuntimeError(
        "Hyperliquid credentials not found: set both HL_ACCOUNT_ADDRESS "
        "and HL_API_WALLET_KEY in the process environment or in "
        "HKEY_CURRENT_USER\\Environment"
    )
