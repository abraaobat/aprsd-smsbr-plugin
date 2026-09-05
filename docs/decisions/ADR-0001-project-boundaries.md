# ADR-0001 — Project boundaries and provider safety

- **Status:** Accepted
- **Date:** 2026-09-04

## Context

SMSBR bridges APRS messages to Brazilian SMS destinations. The project must integrate with APRSD, Dire Wolf/DigiPi and future SMS transports without reimplementing APRS itself or coupling the core command/safety logic to a specific SMS vendor.

The initial public scaffold also needs to prevent accidental real-world SMS delivery before authentication, rate limits and operational controls are validated.

## Decision

1. **APRSD remains the APRS application boundary.** SMSBR is an APRSD plugin/application component and does not implement a new APRS stack.
2. **Dire Wolf and DigiPi are integration paths, not core dependencies.** KISS connectivity is consumed through APRSD.
3. **SMS transports use provider adapters.** The core does not depend directly on one cloud SMS vendor or modem implementation.
4. **`dry-run` is the default provider during pre-alpha.** Real SMS delivery requires an explicit provider configuration and a roadmap phase that validates operational controls.
5. **Authorization and rate limiting live before provider dispatch.** Callsign allow-list, destination normalization and abuse controls cannot be bypassed by a provider implementation.
6. **The public message path is not private.** Secrets and sensitive information must not be transmitted through APRS or stored in logs/config committed to Git.

## Consequences

### Positive

- keeps SMS providers replaceable;
- preserves compatibility with APRSD/Dire Wolf/DigiPi architecture;
- reduces the risk of accidental SMS delivery during development;
- centralizes authorization and abuse controls;
- enables a future GSM/4G modem provider without changing the command domain.

### Trade-offs

- requires provider contract tests;
- APRSD API changes can affect the adapter layer;
- bidirectional SMS → APRS requires additional anti-spoofing and conversation-state design.

## Follow-up

- F2 validates the exact APRSD 5.x plugin/config API.
- F3 selects and validates the first real SMS provider.
- F4 introduces the GSM/4G modem provider behind the same boundary.
