# SMSBR Roadmap

## F0 — Foundation ✅

- Repository architecture
- Apache-2.0 licensing
- README + architecture/protocol/security docs
- Python package scaffold
- GitHub Actions CI
- Changelog
- ADR baseline
- Pull request governance checklist

## F1 — Safe outbound core ✅

- `@DESTINO mensagem` parser
- Brazilian E.164 normalization
- Callsign allow-list
- Aliases
- Per-callsign rate limit
- Dry-run provider
- Unit tests

## F2 — APRSD integration 🟡

- [x] Validate command-plugin API against current APRSD upstream
- [x] Adopt `APRSDRegexCommandPluginBase` + `process(packet)` contract
- [x] Native APRSD / `oslo.config` options
- [x] Export `oslo.config.opts` entry point
- [x] Adapter/config integration tests
- [x] Validate released APRSD and current upstream in CI
- [x] Exercise SMSBR through `aprsd dev test-plugin` with `provider=dry-run`
- [x] Validate APRSD APRS-IS driver/login/send path against an isolated local server
- [x] Validate APRSD TCP KISS driver/frame-send path against an isolated local socket
- [ ] Operational APRS-IS service validation
- [ ] Real Dire Wolf TCP KISS bench validation

F2 remains open until the operational transport paths are validated outside the isolated CI harness. No real SMS provider is enabled during F2, and the deterministic transport smoke never connects to public APRS-IS or keys a radio.

## F3 — First real SMS provider

- Select provider for Brazil
- Outbound adapter
- Delivery-state model
- Timeouts/retries
- Cost guardrails
- Masked logs

## F4 — GSM/4G modem provider

- AT-command modem abstraction
- SIM/network health checks
- SMS submit/result parsing
- Raspberry Pi/DigiPi field test

## F5 — SMS → APRS

- Inbound webhook/modem listener
- Safe conversation/reply mapping
- Opt-in and anti-spoofing controls
- APRS message segmentation and ACK handling

## F6 — National APRS-IS service

- Dedicated service callsign strategy
- APRS-IS filters
- Multi-region monitoring
- Queueing/persistence
- High availability plan

## F7 — Operations, security and compliance

- Abuse controls and destination consent model
- Global limits and emergency shutdown
- Metrics/dashboard
- Data retention policy
- Operational/regulatory review for Brazil

## F8 — Public release

- PyPI package
- Install guide for DigiPi/Dire Wolf
- Docker/systemd deployment
- v1.0 compatibility contract
- Contributor documentation
