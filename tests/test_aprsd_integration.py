from aprsd import plugin
from oslo_config import cfg

from aprsd_smsbr.config import SMSBRConfig
from aprsd_smsbr.conf.main import register_opts
from aprsd_smsbr.plugin import SMSBRPlugin


def test_config_reads_native_oslo_options():
    config = cfg.ConfigOpts()
    register_opts(config)
    config.set_override("enabled", True, group="smsbr_plugin")
    config.set_override(
        "authorized_callsigns", ["pv8abc-7"], group="smsbr_plugin"
    )
    config.set_override(
        "aliases", ["CASA=+5595999999999"], group="smsbr_plugin"
    )
    config.set_override("rate_limit_per_hour", 7, group="smsbr_plugin")

    parsed = SMSBRConfig.from_conf(config)

    assert parsed.enabled is True
    assert parsed.authorized_callsigns == {"PV8ABC-7"}
    assert parsed.aliases == {"CASA": "+5595999999999"}
    assert parsed.rate_limit_per_hour == 7
    assert parsed.provider == "dry-run"


def test_plugin_uses_aprsd_regex_command_api():
    assert issubclass(SMSBRPlugin, plugin.APRSDRegexCommandPluginBase)
    assert SMSBRPlugin.command_regex == r"^@.+"
    assert SMSBRPlugin.command_name == "smsbr"
