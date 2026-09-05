"""SMS provider abstraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class ProviderResult:
    accepted: bool
    message_id: str | None = None
    detail: str | None = None


class SMSProvider(Protocol):
    def send_sms(self, to: str, body: str, *, sender_callsign: str) -> ProviderResult:
        """Submit one SMS for delivery."""
