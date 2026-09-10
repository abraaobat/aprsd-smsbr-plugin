"""APRSD 5.x adapter for SMSBR.

The SMS domain service remains transport-independent. This module only adapts
APRSD MessagePacket handling and oslo.config settings to that service.
"""

from __future__ import annotations

import logging

from aprsd import packets, plugin
from oslo_config import cfg

from . import (
    __version__,
    conf,  # noqa: F401 - importing registers SMSBR oslo.config options
)
from .authorization import AuthorizationPolicy
from .config import SMSBRConfig
from .providers import DryRunSMSProvider
from .ratelimit import SlidingWindowRateLimiter
from .service import SMSBRService

CONF = cfg.CONF
LOG = logging.getLogger("APRSD")


class SMSBRPlugin(plugin.APRSDRegexCommandPluginBase):
    """Send a Brazilian SMS using ``@DESTINO mensagem``."""

    version = __version__
    command_regex = r"^@.+"
    command_name = "smsbr"
    short_description = "Send an SMS to a Brazilian mobile destination"
    enabled = False

    def setup(self):
        try:
            config = SMSBRConfig.from_conf(CONF)
        except Exception as exc:
            LOG.error("Invalid SMSBR configuration: %s", exc)
            self.enabled = False
            return False

        if not config.enabled:
            self.enabled = False
            LOG.info("SMSBR plugin is disabled in config")
            return False

        if config.provider != "dry-run":
            LOG.error(
                "Only provider=dry-run is implemented in %s; disabling SMSBR",
                self.version,
            )
            self.enabled = False
            return False

        self._service = SMSBRService(
            provider=DryRunSMSProvider(),
            authorization=AuthorizationPolicy(config.authorized_callsigns),
            aliases=config.aliases,
            rate_limiter=SlidingWindowRateLimiter(config.rate_limit_per_hour, 3600),
        )
        self.enabled = True
        return True

    def help(self):
        return "smsbr: @DESTINO mensagem"

    def process(self, packet: packets.MessagePacket):
        if not self.enabled:
            return packets.NULL_MESSAGE

        fromcall = packet.get("from")
        message = packet.get("message_text")
        if not fromcall or not message:
            return packets.NULL_MESSAGE

        return self._service.handle(str(fromcall), str(message))
