# SMSBR Roadmap

## F0 — Foundation ✅

- Repository architecture
- Apache-2.0 licensing
- README + architecture/protocol/security docs
- Python package scaffold
- GitHub Actions CI

## F1 — Safe outbound core 🟡

- `@DESTINO mensagem` parser
- Brazilian E.164 normalization
- Callsign allow-list
- Aliases
- Per-callsign rate limit
- Dry-run provider
- Unit tests

## F2 — APRSD 5.x integration

- Validate plugin API against current APRSD 5.x
- Native APRSD/oslo.config options
- Integration test with `aprsd dev` tooling
- Test APRS-IS and TCP KISS/Dire Wolf paths

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
