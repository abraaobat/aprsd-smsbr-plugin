# SMSBR — APRSD Brazilian SMS Gateway

> **Status: pre-alpha / safe scaffold (`0.1.0a0`).** The default provider is `dry-run`; this repository does not send real SMS yet.

SMSBR is an open-source APRSD plugin project for bridging APRS messages to Brazilian
SMS destinations (`+55`). It is designed to work with APRSD and, through APRSD's
KISS support, with Dire Wolf and DigiPi installations.

APRSD itself is designed for APRS services and can use APRS-IS when Internet is
available or a TCP KISS TNC for direct radio connectivity. SMSBR deliberately builds
on that architecture instead of implementing a new APRS stack.

## Proposed flow

```text
Radio/APRS ─► Dire Wolf/KISS ─► APRSD ─► SMSBR ─► SMS provider ─► +55
                      ▲
                    DigiPi

APRS-IS ─────────────────────► APRSD
```

## v0.1 command

```text
@DESTINO mensagem
```

Examples:

```text
@CASA Cheguei bem.
@5595999999999 Teste via APRS.
```

The destination can be a Brazilian number or a configured alias.

## Safety defaults

- Callsigns are **denied by default** until explicitly authorized.
- The initial SMS provider is **dry-run**; no SMS is sent.
- Per-callsign rate limiting is enabled in the core service.
- Secrets and real phone numbers belong in environment/configuration, never Git.
- APRS is not private; do not transmit secrets or sensitive information.

## Development setup

Requires Python 3.11+ because the current APRSD 5.x line requires Python 3.11+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
ruff check .
```

## Prototype configuration

```bash
export SMSBR_PROVIDER=dry-run
export SMSBR_AUTHORIZED_CALLSIGNS=PV8ABC
export SMSBR_ALIASES='CASA=+5595999999999'
export SMSBR_RATE_LIMIT_PER_HOUR=5
```

Then enable the plugin class in your APRSD configuration:

```text
aprsd_smsbr.plugin.SMSBRPlugin
```

See `examples/aprsd.conf.example` and `docs/roadmap.md`.

## Scope

### v0.1

- APRS command parser
- Brazilian number normalization
- Callsign allow-list
- aliases
- rate limiting
- dry-run provider
- APRSD adapter scaffold

### Planned

- real SMS API provider
- USB GSM/4G modem provider
- bidirectional SMS -> APRS
- national APRS-IS deployment model
- DigiPi deployment guide

## Compatibility target

- Python 3.11+
- APRSD 5.x
- Dire Wolf via APRSD KISS
- DigiPi through its APRS/Dire Wolf stack

The APRSD adapter will be validated against the exact current APRSD 5.x plugin API
before the first real SMS provider is enabled.

## Documentation

- [Architecture](docs/architecture.md)
- [Protocol](docs/protocol.md)
- [Security design](docs/security.md)
- [Roadmap](docs/roadmap.md)
- [ADR-0001 — project boundaries and provider safety](docs/decisions/ADR-0001-project-boundaries.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## Governance

- Git is the source of history.
- `pyproject.toml` is the canonical Python package version source.
- Changes use short branches and Conventional Commits.
- Architecture decisions that are difficult to reverse require ADRs.
- CI runs Ruff and pytest on supported Python versions.
- Roadmap and documentation must move with behavior or architecture changes.
- Safe defaults must not be weakened silently.

## License

Apache License 2.0. See `LICENSE`.

---

## English summary

SMSBR is a pre-alpha APRSD plugin project intended to bridge APRS messages to
Brazilian SMS destinations. The initial repository is intentionally safe: delivery
uses a dry-run provider until authentication, rate limits, provider integration and
public-operation controls are validated.
