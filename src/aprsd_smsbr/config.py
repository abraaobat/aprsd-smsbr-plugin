"""SMSBR configuration adapters.

APRSD 5.x uses oslo.config. Environment loading remains available for
standalone/domain tests, but the APRSD plugin path uses ``from_conf``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

from .parser import normalize_br_phone


@dataclass(slots=True)
class SMSBRConfig:
    authorized_callsigns: set[str] = field(default_factory=set)
    aliases: dict[str, str] = field(default_factory=dict)
    rate_limit_per_hour: int = 5
    provider: str = "dry-run"
    enabled: bool = False

    @staticmethod
    def _parse_aliases(items: list[str]) -> dict[str, str]:
        aliases: dict[str, str] = {}
        for item in items:
            if not item.strip() or "=" not in item:
                continue
            name, number = item.split("=", 1)
            aliases[name.strip().upper()] = normalize_br_phone(number.strip())
        return aliases

    @classmethod
    def from_conf(cls, config) -> "SMSBRConfig":
        group = config.smsbr_plugin
        calls = {
            item.strip().upper()
            for item in group.authorized_callsigns
            if item.strip()
        }
        return cls(
            authorized_callsigns=calls,
            aliases=cls._parse_aliases(list(group.aliases)),
            rate_limit_per_hour=group.rate_limit_per_hour,
            provider=group.provider.strip().lower(),
            enabled=group.enabled,
        )

    @classmethod
    def from_env(cls) -> "SMSBRConfig":
        calls = {
            item.strip().upper()
            for item in os.getenv("SMSBR_AUTHORIZED_CALLSIGNS", "").split(",")
            if item.strip()
        }
        aliases = cls._parse_aliases(os.getenv("SMSBR_ALIASES", "").split(","))
        enabled_values = {"1", "true", "yes", "on"}

        return cls(
            authorized_callsigns=calls,
            aliases=aliases,
            rate_limit_per_hour=int(os.getenv("SMSBR_RATE_LIMIT_PER_HOUR", "5")),
            provider=os.getenv("SMSBR_PROVIDER", "dry-run").strip().lower(),
            enabled=os.getenv("SMSBR_ENABLED", "false").strip().lower()
            in enabled_values,
        )
