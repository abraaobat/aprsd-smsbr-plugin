"""Core SMSBR application service, independent from APRSD transport details."""

from __future__ import annotations

from dataclasses import dataclass

from .authorization import AuthorizationPolicy, base_callsign
from .parser import CommandParseError, normalize_br_phone, parse_command
from .providers.base import SMSProvider
from .ratelimit import SlidingWindowRateLimiter


@dataclass(slots=True)
class SMSBRService:
    provider: SMSProvider
    authorization: AuthorizationPolicy
    aliases: dict[str, str]
    rate_limiter: SlidingWindowRateLimiter

    def _resolve_target(self, target: str) -> str:
        alias = self.aliases.get(target.upper())
        if alias:
            return alias
        return normalize_br_phone(target)

    def handle(self, from_callsign: str, message: str) -> str:
        if not self.authorization.is_authorized(from_callsign):
            return "NAO AUTORIZADO"

        key = base_callsign(from_callsign)
        if not self.rate_limiter.allow(key):
            return "LIMITE ATINGIDO"

        try:
            command = parse_command(message)
            target = self._resolve_target(command.target)
        except CommandParseError as exc:
            return str(exc).upper()[:67]

        result = self.provider.send_sms(
            target,
            command.body,
            sender_callsign=from_callsign.upper(),
        )
        if result.accepted:
            return "MSG ACEITA"
        return "FALHA SMS"
