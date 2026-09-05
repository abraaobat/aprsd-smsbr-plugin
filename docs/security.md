# Security and Abuse Model

SMSBR bridges two public or semi-public communications systems, so abuse prevention
is a core requirement rather than an add-on.

## Required controls before real SMS delivery

- Default-deny callsign allow-list.
- Per-callsign rate limiting.
- Global rate limiting / circuit breaker.
- Destination allow-list or opt-in model for public deployments.
- Duplicate-message suppression.
- No API keys, SIM credentials or phone numbers committed to Git.
- Mask destination numbers in logs.
- Audit trail with timestamps and callsigns, with a documented retention policy.
- Explicit provider timeout and retry limits.
- Emergency kill switch for outbound delivery.

## Privacy note

APRS traffic can be publicly observable and archived. Users must not treat APRS as a
private channel. Do not place secrets, authentication codes or sensitive personal
information in SMSBR messages.

## Public-service gate

Do not enable unrestricted national/public access merely because the software can
connect to APRS-IS. Public operation requires an abuse, consent, cost and regulatory
review appropriate to the selected SMS provider and station setup.
