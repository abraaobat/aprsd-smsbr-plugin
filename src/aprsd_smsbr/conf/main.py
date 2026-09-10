"""oslo.config options exported to APRSD 5.x."""

from oslo_config import cfg

SMSBR_GROUP = cfg.OptGroup(
    name="smsbr_plugin",
    title="Options for the SMSBR APRSD plugin",
)

SMSBR_OPTS = [
    cfg.BoolOpt(
        "enabled",
        default=False,
        help="Enable the SMSBR APRSD command plugin.",
    ),
    cfg.ListOpt(
        "authorized_callsigns",
        default=[],
        help="Callsigns allowed to request outbound SMS messages.",
    ),
    cfg.ListOpt(
        "aliases",
        default=[],
        help="Destination aliases as NAME=PHONE entries.",
    ),
    cfg.IntOpt(
        "rate_limit_per_hour",
        default=5,
        min=1,
        help="Maximum accepted SMS requests per base callsign per hour.",
    ),
    cfg.StrOpt(
        "provider",
        default="dry-run",
        help="SMS provider adapter. Only dry-run is implemented in the current alpha.",
    ),
]


def register_opts(config):
    config.register_group(SMSBR_GROUP)
    config.register_opts(SMSBR_OPTS, group=SMSBR_GROUP)


def list_opts():
    return {SMSBR_GROUP.name: SMSBR_OPTS}
