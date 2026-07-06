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
