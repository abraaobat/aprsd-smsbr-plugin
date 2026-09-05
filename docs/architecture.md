# SMSBR Architecture

## Goal

Provide a small, auditable bridge between APRS messages and Brazilian SMS delivery,
while reusing APRSD for APRS message processing and Dire Wolf/DigiPi for radio/KISS.

## Logical flow

```text
APRS RF ─► Dire Wolf/KISS ─► APRSD ─► SMSBR plugin ─► SMS provider ─► +55 handset
                 │               ▲
                 └──── DigiPi ────┘

APRS-IS ────────────────────────► APRSD
```

## Boundaries

- **APRSD** owns APRS-IS/KISS connectivity, packet parsing and APRS replies.
- **SMSBR core** owns command parsing, authorization, aliases and rate limits.
- **Provider adapters** own delivery to a cellular/SMS provider.
- **DigiPi/Dire Wolf** are optional transport infrastructure, not hard dependencies
  of the SMSBR core.

## Design principles

1. Default-deny authorization.
2. Dry-run provider is the default until a real SMS adapter is explicitly enabled.
3. Phone numbers are normalized to Brazilian E.164 form.
4. Phone numbers should be masked in operational logs.
5. APRS replies should remain short enough for practical packet-radio use.
6. Provider code must not be coupled to APRSD internals.
