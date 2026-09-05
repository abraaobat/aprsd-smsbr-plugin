## Summary

Describe the change and why it is needed.

## Validation

- [ ] `ruff check .`
- [ ] `pytest`
- [ ] Documentation updated when behavior, configuration or architecture changed
- [ ] Roadmap updated when phase/status changed
- [ ] No secrets or real phone numbers were committed

## Safety

- [ ] `dry-run` remains the safe default, or this PR explicitly belongs to the validated real-provider phase
- [ ] Callsign authorization and rate limiting are not bypassed
- [ ] Logs/configuration do not expose sensitive values

## Architecture

- [ ] No ADR required
- [ ] ADR added/updated because this change is difficult to reverse
