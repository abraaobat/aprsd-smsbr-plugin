# SMSBR APRS Message Protocol

## v0.1 outbound command

Send an APRS message to the callsign/service running SMSBR with:

```text
@DESTINO mensagem
```

`DESTINO` can be a Brazilian phone number or a configured alias.

Examples:

```text
@CASA Cheguei ao local.
@5595999999999 Teste via APRS.
```

## Replies

The prototype uses compact Portuguese status replies:

- `MSG ACEITA`
- `NAO AUTORIZADO`
- `LIMITE ATINGIDO`
- `NUMERO BR INVALIDO`
- `FALHA SMS`

`MSG ACEITA` means the configured provider accepted the submission. It does **not**
mean the carrier has confirmed final handset delivery.

## Future inbound syntax

The SMS -> APRS direction is intentionally deferred to a later phase. A reply-token
or conversation mapping will be designed before enabling public inbound traffic.
