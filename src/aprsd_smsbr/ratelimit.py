"""Small in-memory rate limiter for the prototype."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
import time


@dataclass(slots=True)
class SlidingWindowRateLimiter:
    limit: int = 5
    window_seconds: int = 3600
    _events: dict[str, deque[float]] = field(
        default_factory=lambda: defaultdict(deque), init=False
    )

    def allow(self, key: str, now: float | None = None) -> bool:
        now = time.time() if now is None else now
        events = self._events[key]
        cutoff = now - self.window_seconds
        while events and events[0] <= cutoff:
            events.popleft()
        if len(events) >= self.limit:
            return False
        events.append(now)
        return True
