import pytest

from aprsd_smsbr.parser import CommandParseError, normalize_br_phone, parse_command


def test_parse_phone_command():
    cmd = parse_command("@5595999999999 Cheguei bem")
    assert cmd.target == "5595999999999"
    assert cmd.body == "Cheguei bem"


def test_parse_alias_command():
    cmd = parse_command("@casa Tudo certo")
    assert cmd.target == "CASA"


def test_normalize_br_phone_national():
    assert normalize_br_phone("95 99999-9999") == "+5595999999999"


def test_normalize_br_phone_e164():
    assert normalize_br_phone("+55 95 99999-9999") == "+5595999999999"


def test_invalid_command():
    with pytest.raises(CommandParseError):
        parse_command("sem prefixo")
