"""Prototype configuration loaded from environment variables."""

from __future__ import annotations

from dataclasses import dataclass, field
import os

from .parser import normalize_br_phone


@dataclass(slots=True)
class SMSBRConfig:
    authorized_callsigns: set[str] = field(default_factory=set)
    aliases: dict[str, str] = field(default_factory=dict)
    rate_limit_per_hour: int = 5
    provider: str = "dry-run"

    @classmethod
    def from_env(cls) -> "SMSBRConfig":
        calls = {
            item.strip().upper()
            for item in os.getenv("SMSBR_AUTHORIZED_CALLSIGNS", "").split(",")
            if item.strip()
        }
        aliases: dict[str, str] = {}
        for item in os.getenv("SMSBR_ALIASES", "").split(","):
            if not item.strip() or "=" not in item:
                continue
            name, number = item.split("=", 1)
            aliases[name.strip().upper()] = normalize_br_phone(number.strip())

        return cls(
            authorized_callsigns=calls,
            aliases=aliases,
            rate_limit_per_hour=int(os.getenv("SMSBR_RATE_LIMIT_PER_HOUR", "5")),
            provider=os.getenv("SMSBR_PROVIDER", "dry-run").strip().lower(),
        )
