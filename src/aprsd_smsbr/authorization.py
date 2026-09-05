"""Authorization helpers for callsigns."""

from __future__ import annotations

from dataclasses import dataclass, field


def base_callsign(callsign: str) -> str:
    """Return the base callsign, ignoring an APRS SSID suffix."""
    return (callsign or "").strip().upper().split("-", 1)[0]


@dataclass(slots=True)
class AuthorizationPolicy:
    """Simple allow-list policy for the first public prototype."""

    authorized_callsigns: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        self.authorized_callsigns = {
            base_callsign(item) for item in self.authorized_callsigns if item.strip()
        }

    def is_authorized(self, callsign: str) -> bool:
        if not self.authorized_callsigns:
            return False
        return base_callsign(callsign) in self.authorized_callsigns
