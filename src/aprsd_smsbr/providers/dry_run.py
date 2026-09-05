"""Non-delivering provider used for development and safe tests."""

from __future__ import annotations

from uuid import uuid4

from .base import ProviderResult


class DryRunSMSProvider:
    def send_sms(self, to: str, body: str, *, sender_callsign: str) -> ProviderResult:
        del to, body, sender_callsign
        return ProviderResult(accepted=True, message_id=f"dry-{uuid4().hex[:10]}")
