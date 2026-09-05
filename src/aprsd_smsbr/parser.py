"""Parse compact SMSBR commands carried inside APRS messages."""

from __future__ import annotations

from dataclasses import dataclass
import re


class CommandParseError(ValueError):
    """Raised when an SMSBR APRS command is malformed."""


@dataclass(frozen=True, slots=True)
class SMSBRCommand:
    target: str
    body: str


_COMMAND_RE = re.compile(
    r"^\s*@(?P<target>[A-Za-z0-9+_-]{2,32})\s+(?P<body>\S(?:.*\S)?)\s*$"
)


def parse_command(message: str) -> SMSBRCommand:
    """Parse ``@TARGET message`` from an APRS message body."""
    match = _COMMAND_RE.match(message or "")
    if not match:
        raise CommandParseError("Use @DESTINO mensagem")

    body = match.group("body").strip()
    if not body:
        raise CommandParseError("Mensagem vazia")

    return SMSBRCommand(target=match.group("target").upper(), body=body)


def normalize_br_phone(value: str) -> str:
    """Normalize a Brazilian number to E.164 (+55...).

    Accepted forms intentionally avoid carrier prefixes and ambiguous trunk forms:
    +55DDXXXXXXXX(X), 55DDXXXXXXXX(X), or DDXXXXXXXX(X).
    """
    raw = value.strip()
    if raw.startswith("+"):
        raw = raw[1:]
    digits = re.sub(r"\D", "", raw)

    if digits.startswith("55") and len(digits) in (12, 13):
        national = digits[2:]
    elif len(digits) in (10, 11):
        national = digits
    else:
        raise CommandParseError("Numero BR invalido")

    ddd = national[:2]
    subscriber = national[2:]
    if ddd.startswith("0") or len(subscriber) not in (8, 9):
        raise CommandParseError("Numero BR invalido")

    return f"+55{national}"
