class AlreadyRegisteredError(Exception):
    pass


class InvalidQuestionError(Exception):
    pass


class ThemeNotFoundError(Exception):
    pass


class ValidationError(Exception):
    """
    Exception raised when validation fails.
    """
    def __init__(self, message):
        super(ValidationError, self).__init__()
        self._message = message

    def __str__(self):
        return self._message

    @property
    def message(self):
        return self._message
