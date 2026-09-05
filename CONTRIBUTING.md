# Contributing

1. Create a focused branch.
2. Add or update tests for behavior changes.
3. Run `pytest` and `ruff check .`.
4. Never commit real SMS credentials, SIM secrets or private phone lists.
5. Open a pull request describing the radio/APRS and SMS-side impact.

Security-sensitive changes (authorization, inbound SMS, public APRS-IS operation,
rate limits or secrets handling) require explicit review before merge.
