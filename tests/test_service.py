from aprsd_smsbr.authorization import AuthorizationPolicy
from aprsd_smsbr.providers import DryRunSMSProvider
from aprsd_smsbr.ratelimit import SlidingWindowRateLimiter
from aprsd_smsbr.service import SMSBRService


def make_service(limit=5):
    return SMSBRService(
        provider=DryRunSMSProvider(),
        authorization=AuthorizationPolicy({"PV8ABC"}),
        aliases={"CASA": "+5595999999999"},
        rate_limiter=SlidingWindowRateLimiter(limit=limit, window_seconds=3600),
    )


def test_authorized_ssid_is_accepted():
    service = make_service()
    assert service.handle("PV8ABC-7", "@CASA teste") == "MSG ACEITA"


def test_unauthorized_callsign_is_rejected():
    service = make_service()
    assert service.handle("PY2XYZ", "@CASA teste") == "NAO AUTORIZADO"


def test_rate_limit():
    service = make_service(limit=1)
    assert service.handle("PV8ABC", "@CASA primeira") == "MSG ACEITA"
    assert service.handle("PV8ABC", "@CASA segunda") == "LIMITE ATINGIDO"
