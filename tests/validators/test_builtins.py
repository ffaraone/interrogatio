import pytest

from interrogatio.core.exceptions import ValidationError
from interrogatio.validators.builtins import (
    DateTimeRangeValidator,
    DateTimeValidator,
    EmailValidator,
    IntegerValidator,
    IPv4Validator,
    MaxLengthValidator,
    MaxValidator,
    MinLengthValidator,
    MinValidator,
    NumberValidator,
    RangeValidator,
    RegexValidator,
    RequiredValidator,
    URLValidator,
)


@pytest.mark.parametrize(
    'value',
    (
        '10.0.0.1',
        '192.168.1.1',
        '192.168.1.255',
    ),
)
def test_validate_ipv4_address(value):
    v = IPv4Validator()
    assert v.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (
        '10.0.0.256',
        '255.255',
        'a.b.c.d',
    ),
)
def test_validate_ipv4_address_invalid(value):
    v = IPv4Validator()
    with pytest.raises(ValidationError):
        v.validate(value)


@pytest.mark.parametrize(
    'value',
    (
        'a',
        'd sd d',
        ('a',),
        ('a', 'b'),
        ['a'],
        [1, 2, 3],
        {'a': 'v'},
        {'b': 'a', 'a': 'b'},
    ),
)
def test_required_validator(value):
    r = RequiredValidator()
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (
        None,
        False,
        '',
        tuple(),
        [],
        {},
    ),
)
def test_required_validator_invalid(value):
    r = RequiredValidator()
    with pytest.raises(ValidationError):
        r.validate(value)


def test_regex_validator():
    r = RegexValidator(r'^[a-zA-Z]+$')
    assert r.validate('aianaBCBCyasgfdBCbB') is None


def test_regex_validator_invalid():
    r = RegexValidator(r'^[a-zA-Z]+$')
    with pytest.raises(ValidationError):
        r.validate('aianaBCBCya111')

    with pytest.raises(ValidationError):
        r.validate('a##')


@pytest.mark.parametrize(
    'value',
    (
        None,
        '',
        'gigi@日本語.org',
        'test@gmail.com',
        'hello@microsoft.com',
    ),
)
def test_email_validator(value):
    r = EmailValidator()
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (
        '日本語.idn.icann.org',
        'microsoft.com',
        'test@domain',
    ),
)
def test_email_validator_invalid(value):
    r = EmailValidator()
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (
        'https://www.日本語.com',
        'https://gmail.com',
        'http://test.app.microsoft.com',
        'https://www.日本語.com:8443',
        'https://gmail.com:9443',
        'http://user:pass@test.app.microsoft.com',
        'ftp://test.local',
    ),
)
def test_url_validator(value):
    r = URLValidator()
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (
        'https://' + 'a' * 254,
        'https://test',
        'my.url.com',
    ),
)
def test_url_validator_invalid(value):
    r = URLValidator()
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (
        '',
        [],
        'a' * 99,
        'b' * 100,
        ['x' for _ in range(99)],
        ['x' for _ in range(100)],
    ),
)
def test_maxlength_validator(value):
    r = MaxLengthValidator(100)
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (
        'a' * 99,
        'b' * 100,
        ['x' for _ in range(99)],
        ['x' for _ in range(100)],
        66,
    ),
)
def test_maxlength_validator_invalid(value):
    r = MaxLengthValidator(98)
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (
        '0' * 98,
        'a' * 99,
        'b' * 100,
        ['x' for _ in range(98)],
        ['x' for _ in range(99)],
        ['x' for _ in range(100)],
    ),
)
def test_minlength_validator(value):
    r = MinLengthValidator(98)
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (
        'a' * 99,
        'b' * 100,
        ['x' for _ in range(99)],
        ['x' for _ in range(100)],
        25,
    ),
)
def test_minlength_validator_invalid(value):
    r = MinLengthValidator(101)
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 20.93, -11.2994, 0xff12, 0o7146, 0b11010011),
)
def test_number_validator(value):
    r = NumberValidator()
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    ('', 'string', list(), list([1, 2, 3]), dict()),
)
def test_number_validator_invalid(value):
    r = NumberValidator()
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 0xff12, 0o7146, 0b11010011),
)
def test_integer_validator(value):
    r = IntegerValidator()
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    ('-1', '0', '1', 20.93, -11.2994, [1, 2, 3]),
)
def test_integer_validator_invalid(value):
    r = IntegerValidator()
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 3.88, 0o10, 0b1000, 0x0F),
)
def test_min_validator(value):
    r = MinValidator(-2)
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (-3.88, -0o10, -0b1000, -0x0F, [1, 2, 3]),
)
def test_min_validator_invalid(value):
    r = MinValidator(-2)
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 3.88, 0o10, 0b1000, 0x0F),
)
def test_max_validator(value):
    r = MaxValidator(16)
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 3.88, 0o10, 0b1000, 0x0F, [1, 2, 3]),
)
def test_max_validator_invalid(value):
    r = MaxValidator(-2)
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 3.88, 0o10, 0b1000, 0x0F),
)
def test_range_validator(value):
    r = RangeValidator(-2, 16)
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 3.88, 0o10, 0b1000, 0x0F, [1, 2, 3]),
)
def test_range_validator_invalid(value):
    r = RangeValidator(-20, -2)
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (
        '2020-01-01T12:00:00',
        '2020-02-29T23:00:00',
        '',
        None,
    ),
)
def test_date_validator(value):
    r = DateTimeValidator()
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (-1, 0, 1, 3.88, 0o10, 0b1000, 0x0F, [1, 2, 3], '2020-02-30T23:00:00'),
)
def test_date_validator_invalid(value):
    r = DateTimeValidator()
    with pytest.raises(ValidationError):
        r.validate(value)


@pytest.mark.parametrize(
    'value',
    (
        {'from': '2020-01-01T12:00:00', 'to': '2020-03-01T12:00:00'},
        {'from': '2020-01-01T12:00:00', 'to': ''},
        {'from': None, 'to': '2020-03-01T12:00:00'},
        '',
        None,
    ),
)
def test_daterange_validator(value):
    r = DateTimeRangeValidator(format_pattern='%Y-%m-%dT%H:%M:%S')
    assert r.validate(value) is None


@pytest.mark.parametrize(
    'value',
    (
        {'from': '2020-01-01T12:00:00', 'to': '2019-03-01T12:00:00'},
        {'from': 'xxxx', 'to': 'xxxx'},
        [1, 2, 3],
    ),
)
def test_daterange_validator_invalid(value):
    r = DateTimeRangeValidator(format_pattern='%Y-%m-%dT%H:%M:%S')
    with pytest.raises(ValidationError):
        r.validate(value)
