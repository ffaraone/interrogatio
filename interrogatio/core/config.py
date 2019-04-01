__all__ = ['get_config']

class Config:

    def __init__(self):
        self._prompt_question_mark = '?'
        self._dialog_question_mark = ''
        self._selectone_symbol = '(\u2713)'
        self._selectmany_symbol = '[\u2713]'

    @property
    def prompt_question_mark(self):
        return self._prompt_question_mark

    @prompt_question_mark.setter
    def prompt_question_mark(self, value):
        self._prompt_question_mark = value

    @property
    def dialog_question_mark(self):
        return self._dialog_question_mark

    @dialog_question_mark.setter
    def dialog_question_mark(self, value):
        self._dialog_question_mark = value
    

    @property
    def selectone_symbol(self):
        return self._selectone_symbol

    @selectone_symbol.setter
    def selectone_symbol(self, value):
        self._selectone_symbol = value

    @property
    def selectmany_symbol(self):
        return self._selectmany_symbol

    @selectmany_symbol.setter
    def selectmany_symbol(self, value):
        self._selectmany_symbol = value


_config = Config()


def get_config():
    return _config
