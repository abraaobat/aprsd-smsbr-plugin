"""APRSD adapter for SMSBR.

The core service is intentionally transport-independent. This adapter follows the
APRSD command-plugin API used by the APRSD plugin ecosystem. It is kept thin so
future APRSD API changes do not affect the SMSBR domain logic.
"""

from __future__ import annotations

from aprsd import plugin

from .authorization import AuthorizationPolicy
from .config import SMSBRConfig
from .providers import DryRunSMSProvider
from .ratelimit import SlidingWindowRateLimiter
from .service import SMSBRService


class SMSBRPlugin(plugin.APRSDPluginBase):
    """Send a Brazilian SMS using ``@DESTINO mensagem``."""

    version = "0.1.0a0"
    command_regex = r"^@.+"
    command_name = "smsbr"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cfg = SMSBRConfig.from_env()
        if cfg.provider != "dry-run":
            raise RuntimeError(
                "Only SMSBR_PROVIDER=dry-run is implemented in v0.1.0a0"
            )
        self._service = SMSBRService(
            provider=DryRunSMSProvider(),
            authorization=AuthorizationPolicy(cfg.authorized_callsigns),
            aliases=cfg.aliases,
            rate_limiter=SlidingWindowRateLimiter(cfg.rate_limit_per_hour, 3600),
        )

    def command(self, fromcall, message, ack):
        del ack
        return self._service.handle(fromcall, message)
