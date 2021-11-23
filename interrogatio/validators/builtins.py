import re
from datetime import datetime

import validators

from interrogatio.core.exceptions import ValidationError
from interrogatio.validators.base import Validator
from interrogatio.validators.registry import register


__all__ = [
    'RequiredValidator',
    'RegexValidator',
    'URLValidator',
    'EmailValidator',
    'MinLengthValidator',
    'MaxLengthValidator',
    'NumberValidator',
    'IntegerValidator',
    'IPv4Validator',
    'RangeValidator',
    'MinValidator',
    'MaxValidator',
    'DateTimeValidator',
    'DateTimeRangeValidator',
]


@register('required')
class RequiredValidator(Validator):
    def __init__(self, message=None):
        """
        Initialise the ``required`` validator.

        :param message: the error message in case that validation fails.
        :type message: str
        """
        super(RequiredValidator, self).__init__(
            message=message or 'this field is required',
        )

    def validate(self, value, context=None):
        if not value:
            raise ValidationError(self.message)


@register('regex')
class RegexValidator(Validator):
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
        super(RegexValidator, self).__init__(
            message=message or f'this field does not match {expr}',
        )
        self.regex = re.compile(expr)
        self.inverse_match = inverse_match

    def validate(self, value, context=None):
        regex_matches = self.regex.search(str(value))
        invalid_input = (
            regex_matches if self.inverse_match else not regex_matches
        )
        if invalid_input:
            raise ValidationError(self.message)


@register('email')
class EmailValidator(Validator):

    def __init__(self, message=None):
        """
        Initialise the ``email`` validator.
        :param message: the error message in case that validation fails.
        :type message: str
        """
        super(EmailValidator, self).__init__(
            message=message or 'this field must be an email address',
        )

    def validate(self, value, context=None):
        if value and validators.email(value) is not True:
            raise ValidationError(self.message)


@register('url')
class URLValidator(Validator):

    def __init__(self, message=None):
        super().__init__(message=message or 'this field must be an url')

    def validate(self, value, context=None):
        if value and validators.url(value) is not True:
            raise ValidationError(self.message)


@register('min-length')
class MinLengthValidator(Validator):
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
        self.message = message or (
            'the length of this field must be at '
            'least {} characters long'.format(self.min_length)
        )

    def validate(self, value, context=None):
        try:
            if (
                value
                and validators.length(value, min=self.min_length) is not True
            ):
                raise ValidationError(message=self.message)
        except (TypeError, AssertionError):
            raise ValidationError(message=self.message)


@register('max-length')
class MaxLengthValidator(Validator):
    def __init__(self, max_length, message=None):
        """
        Initialise the ``max-length`` validator.

        :param max_length: Maximum length from which the value has to be
                           considered invalid.
        :type max_length: int
        :param message: the error message in case that validation fails.
        :type message: str
        """
        self.max_length = max_length
        self.message = message or (
            'the length of this field must be at '
            f'most {max_length} characters long'
        )

    def validate(self, value, context=None):
        try:
            if (
                value
                and validators.length(value, max=self.max_length) is not True
            ):
                raise ValidationError(message=self.message)
        except (TypeError, AssertionError):
            raise ValidationError(message=self.message)


@register('number')
class NumberValidator(Validator):
    def __init__(self, message=None):
        self.message = message or 'this field must be a number'

    def validate(self, value, context=None):
        try:
            float(value)
        except (ValueError, TypeError):
            raise ValidationError(message=self.message)


@register('integer')
class IntegerValidator(Validator):
    def __init__(self, message=None):
        self.message = message or 'this field must be an integer'

    def validate(self, value, context=None):
        try:
            int(value)
        except (ValueError, TypeError):
            raise ValidationError(message=self.message)

        if int(value) != value:
            raise ValidationError(message=self.message)


@register('ipv4')
class IPv4Validator(Validator):
    def __init__(self, message=None):
        self.message = message or 'this field must be an IPv4 address'

    def validate(self, value, context=None):
        if value and validators.ipv4(value) is not True:
            raise ValidationError(message=self.message)


@register('range')
class RangeValidator(Validator):
    def __init__(self, min=None, max=None, message=None):
        self.min = min
        self.max = max
        self.message = message or (
            f'this field must be a number between {min} and {max}'
        )

    def validate(self, value, context=None):
        try:
            if (
                value is not None and value != ''
                and validators.between(
                    value,
                    min=self.min,
                    max=self.max,
                ) is not True
            ):
                raise ValidationError(message=self.message)
        except (TypeError, AssertionError):
            raise ValidationError(message=self.message)


@register('min')
class MinValidator(Validator):
    def __init__(self, min=None, message=None):
        self.min = min
        self.message = (
            message or f'this field must be greater or equal to {min}'
        )

    def validate(self, value, context=None):
        try:
            if (
                value is not None and value != ''
                and validators.between(
                    value,
                    min=self.min,
                ) is not True
            ):
                raise ValidationError(message=self.message)
        except (TypeError, AssertionError):
            raise ValidationError(message=self.message)


@register('max')
class MaxValidator(Validator):
    def __init__(self, max=None, message=None):
        self.max = max
        self.message = (
            message or f'this field must be smaller or equal to {max}'
        )

    def validate(self, value, context=None):
        try:
            if (
                value is not None and value != ''
                and validators.between(
                    value,
                    max=self.max,
                ) is not True
            ):
                raise ValidationError(message=self.message)
        except (TypeError, AssertionError):
            raise ValidationError(message=self.message)


@register('datetime')
class DateTimeValidator(Validator):
    def __init__(self, format_pattern='%Y-%m-%dT%H:%M:%S', message=None):
        self.format_pattern = format_pattern
        self.message = message or 'this field is not a valid datetime'

    def validate(self, value, context=None):
        if value is None or value == '':
            return
        try:
            datetime.strptime(value, self.format_pattern)
        except (TypeError, ValueError):
            raise ValidationError(message=self.message)


@register('datetimerange')
class DateTimeRangeValidator(Validator):
    def __init__(self, format_pattern='%Y-%m-%d', message=None):
        self.format_pattern = format_pattern
        self.message = message or 'this field is not a valid datetime range'

    def validate(self, value, context=None):
        if value is None or value == '':
            return
        d_from = None
        d_to = None
        try:
            if value['from']:
                d_from = datetime.strptime(value['from'], self.format_pattern)
            if value['to']:
                d_to = datetime.strptime(value['to'], self.format_pattern)
        except (TypeError, ValueError):
            raise ValidationError(message=self.message)

        if d_from and d_to:
            if d_from > d_to:
                raise ValidationError(message=self.message)
