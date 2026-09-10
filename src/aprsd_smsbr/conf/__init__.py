"""APRSD/oslo.config registration for SMSBR."""

from oslo_config import cfg

from .main import list_opts, register_opts

CONF = cfg.CONF
register_opts(CONF)

__all__ = ["CONF", "list_opts", "register_opts"]
