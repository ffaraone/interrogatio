import abc
import collections
import ipaddress
import re
from urllib.parse import urlsplit, urlunsplit

import six

from ..core.validation import ValidationContext

__all__ = [
    'ValidationError',
    'Validator',
    'RequiredValidator',
    'RegexValidator',
    'URLValidator',
    'EmailValidator',
    'MinLengthValidator',
    'MaxLengthValidator',
    'ExactLengthValidator',
    'NumberValidator',
    'IntegerValidator',
    'IPv4Validator',
    'RangeValidator',
    'MinValidator',
    'MaxValidator'
]


class ValidationError(Exception):
    """
    Exception raised when validation fails.
    """
    def __init__(self, message):
        self._message = message
    
    def __str__(self):
        return self._message

    @property
    def message(self):
        return self._message


class Validator(six.with_metaclass(abc.ABCMeta, object)):
    """
    Abstract class for validators. 

    .. note::  
        Subclasses must provide a ``ALIAS`` static member with the name 
        of the validator.
        Validator aliases must be unique.
    """
    def __init__(self, message='invalid input'):
        self.message = message

    @abc.abstractmethod
    def validate(self, value, context):
        """
        Abstract method.
        Subclasses must implement this method with the validation logic.

        :param value: the value to validate.
        :type value: str

        :raises: 
            ValidationError: if the provided input is invalid.
        """
        if not isinstance(context, ValidationContext):
            raise ValueError('context must be a ValidationContext instance')


def _validate_ipv4_address(value):
    try:
        ipaddress.IPv4Address(value)
    except ValueError:
        raise ValidationError('invalid IPv4 address')

def _validate_ipv6_address(value):
    try:
        ipaddress.IPv6Address(value)
    except ValueError:
        raise ValidationError('invalid IPv6 address')


def validate_ipv46_address(value):
    try:
        _validate_ipv4_address(value)
    except ValidationError:
        try:
            _validate_ipv6_address(value)
        except ValidationError:
            raise ValidationError(message='invalid IPv4 or IPv6 address')


class RequiredValidator(Validator):
    ALIAS = 'required'
    def __init__(self, message=None):
        """
        Initialise the ``required`` validator.

        :param message: the error message in case that validation fails.
        :type message: str
        """
        self.message = message or 'this field is required'

    def validate(self, value, context):
        if value.strip():
            return
        raise ValidationError(self.message)


class RegexValidator(Validator):
    ALIAS = 'regex'
    def __init__(self, expr, message=None, inverse_match=None):
        """
        Initialise the ``regex`` validator.

        :param expr: the regex to match.
        :type expr: str
        :param message: the error message in case that validation fails.
        :type message: str
        :param inverse_match: invert the match of the expression.
        :type inverse_match: bool
        """
        if expr:
            self.regex = re.compile(expr)
            self.message = message or 'this field does not match {}'.format(
                expr)
        self.inverse_match = inverse_match

    def validate(self, value, context):
        regex_matches = self.regex.search(str(value))
        invalid_input = regex_matches if self.inverse_match else not regex_matches
        if invalid_input:
            raise ValidationError(self.message)


class EmailValidator(Validator):
    ALIAS = 'email'
    user_regex = re.compile(
        r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
        r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
        re.IGNORECASE)
    domain_regex = re.compile(
        # max length for domain name labels is 63 characters per RFC 1034
        r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
        re.IGNORECASE)
    literal_regex = re.compile(
        # literal form, ipv4 or ipv6 address (SMTP 4.1.3)
        r'\[([A-f0-9:\.]+)\]\Z',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    def __init__(self, whitelist=None, message=None):
        """
        Initialise the ``email`` validator.

        :param whitelist: an optiona whitelist of domain names to be 
                          considered valid.
        :type whitelist: list
        :param message: the error message in case that validation fails.
        :type message: str
        """
        self.message = message or 'this field must be an email address'
        if whitelist is not None:
            self.domain_whitelist = whitelist

    def validate(self, value, context):
        if not value or '@' not in value:
            raise ValidationError(self.message)

        user_part, domain_part = value.rsplit('@', 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(message=self.message)

        if (domain_part not in self.domain_whitelist and
                not self.validate_domain_part(domain_part)):
            # Try for possible IDN domain-part
            try:
                domain_part = domain_part.encode('idna').decode('ascii')
            except UnicodeError:
                pass
            else:
                if self.validate_domain_part(domain_part):
                    return
            raise ValidationError(self.message)

    def validate_domain_part(self, domain_part):
        if self.domain_regex.match(domain_part):
            return True

        literal_match = self.literal_regex.match(domain_part)
        if literal_match:
            ip_address = literal_match.group(1)
            try:
                validate_ipv46_address(ip_address)
                return True
            except ValidationError:
                pass
        return False


class URLValidator(Validator):
    ALIAS = 'url'
    ul = '\u00a1-\uffff'  # unicode letters range (must not be a raw string)

    # IP patterns
    ipv4_re = r'(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}'
    ipv6_re = r'\[[0-9a-f:\.]+\]'  # (simple regex, validated later)

    # Host patterns
    hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
    # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
    domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
    tld_re = (
        r'\.'                                # dot
        r'(?!-)'                             # can't start with a dash
        r'(?:[a-z' + ul + '-]{2,63}'         # domain label
        r'|xn--[a-z0-9]{1,59})'              # or punycode label
        r'(?<!-)'                            # can't end with a dash
        r'\.?'                               # may have a trailing dot
    )
    host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'

    regex = re.compile(
        r'^(?:[a-z0-9\.\-\+]*)://'  # scheme is validated separately
        r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'  # user:pass authentication
        r'(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')'
        r'(?::\d{2,5})?'  # port
        r'(?:[/?#][^\s]*)?'  # resource path
        r'\Z', re.IGNORECASE)
    schemes = ['http', 'https', 'ftp', 'ftps']
    message = 'the URL is invalid'

    def __init__(self, schemes=None, **kwargs):
        """
        Initialise the ``url`` validator.

        :param schemes: an optional list of url schemes
        :type schemes: list
        :param message: the error message in case that validation fails.
        :type message: str
        """
        super().__init__(**kwargs)
        if schemes is not None:
            self.schemes = schemes
        
    def validate(self, value, context):
        scheme = value.split('://')[0].lower()
        if scheme not in self.schemes:
            raise ValidationError(message=self.message)

        # Then check full URL
        try:
            super().validate(value, context)
        except ValidationError as e:
            # Trivial case failed. Try for possible IDN domain
            if value:
                try:
                    scheme, netloc, path, query, fragment = urlsplit(value)
                except ValueError:  # for example, "Invalid IPv6 URL"
                    raise ValidationError(message=self.message)
                try:
                    netloc = netloc.encode('idna').decode('ascii')  # IDN -> ACE
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super().validate(url, context)
            else:
                raise
        else:
            # Now verify IPv6 in the netloc part
            host_match = re.search(r'^\[(.+)\](?::\d{2,5})?$', urlsplit(value).netloc)
            if host_match:
                potential_ip = host_match.groups()[0]
                try:
                    _validate_ipv6_address(potential_ip)
                except ValidationError:
                    raise ValidationError(message=self.message)

        # The maximum length of a full host name is 253 characters per RFC 1034
        # section 3.1. It's defined to be 255 bytes or less, but this includes
        # one byte for the length of the name and one byte for the trailing dot
        # that's used to indicate absolute names in DNS.
        if len(urlsplit(value).netloc) > 253:
            raise ValidationError(message=self.message)


# class MatchFieldValidator(Validator):
#     def __init__(self, field, message=None):
#         self.field = field
#         self.message = message or 'this field does not match {}'.format(field)

#     def __call__(self, document, context):
#         valid = document and context and document == context.get(self.field)    
#         if not valid:
#             raise ValidationError(message=self.message)

class MinLengthValidator(Validator):
    ALIAS = 'min-length'
    def __init__(self, min_length, message=None):
        """
        Initialise the ``min-length`` validator.

        :param min_length: Minumum length from which the value has to be 
                           considered valid.
        :type min_length: int
        :param message: the error message in case that validation fails.
        :type message: str
        """

        self.min_length = min_length
        self.message = message or 'the length of this field must be at '\
            'least {} characters long'.format(self.min_length)

    def validate(self, value, context):
        if len(value) < self.min_length:
            raise ValidationError(message=self.message)

class MaxLengthValidator(Validator):
    ALIAS = 'max-length'
    def __init__(self, max_length, message=None):
        """
        Initialise the ``max-length`` validator.

        :param min_length: Maximum length from which the value has to be 
                           considered invalid.
        :type max_length: int
        :param message: the error message in case that validation fails.
        :type message: str
        """
        self.max_length = max_length
        self.message = message or 'the length of this field must be at '\
            'most {} characters long'.format(self.max_length)

    def validate(self, value, context):
        if len(value) > self.max_length:
            raise ValidationError(message=self.message)


class ExactLengthValidator(Validator):
    ALIAS = 'exact-length'
    def __init__(self, length=None, message=None):
        self.length = length
        self.message = message or 'the length of this field must be '\
            '{} characters long'.format(self.length)

    def validate(self, value, context):
        if len(value) > self.length:
            raise ValidationError(message=self.message)


class NumberValidator(Validator):
    ALIAS = 'number'
    def __init__(self, message=None):
        self.message = message or 'this field must be a number'

    def validate(self, value, context):
        try:
            float(value)
        except ValueError:
            raise ValidationError(message=self.message)

class IntegerValidator(Validator):
    ALIAS = 'integer'
    def __init__(self, message=None):
        self.message = message or 'this field must be an integer'

    def validate(self, value, context):
        try:
            int(value)
        except ValueError:
            raise ValidationError(message=self.message)


class IPv4Validator(Validator):
    ALIAS = 'ipv4'
    def __init__(self, message=None):
        self.message = message or 'this field must be an IPv4 address'

    def validate(self, value, context):
        try:
            ipaddress.IPv4Address(value)
        except ValueError:
            raise ValidationError(message=self.message)


class RangeValidator(Validator):
    ALIAS = 'range'
    def __init__(self, min=None, max=None, message=None):
        self.min = float(min)
        self.max = float(max)
        self.message = message or \
            'this field must be a number between {} and {}'.format(min, max)
    def validate(self, value, context):
        try:
            value = float(value)
            if value < self.min or value > self.max:
                raise ValidationError(message=self.message)
        except ValueError:
            raise ValidationError(message=self.message)

class MinValidator(Validator):
    ALIAS = 'min'
    def __init__(self, min=None, message=None):
        self.min = float(min)
        self.message = message or \
            'this field must be greater or equal to {}'.format(min)
    def validate(self, value, context):
        try:
            value = float(value)
            if value < self.min:
                raise ValidationError(message=self.message)
        except ValueError:
            raise ValidationError(message=self.message)

class MaxValidator(Validator):
    ALIAS = 'max'
    def __init__(self, max=None, message=None):
        self.max = float(max)
        self.message = message or \
            'this field must be smaller or equal to {}'.format(max)
    def validate(self, value, context):
        try:
            value = float(value)
            if value > self.max:
                raise ValidationError(message=self.message)
        except ValueError:
            raise ValidationError(message=self.message)