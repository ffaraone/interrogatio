import json

from prompt_toolkit.styles import Style, default_ui_style, merge_styles

from ..core.exceptions import AlreadyRegisteredError, ThemeNotFoundError

__all__ = [
    'Theme',
    'register',
    'for_dialog',
    'for_prompt',
    'set_theme'
]


class Theme:

    def __init__(self):
        self._prompt_styles = dict()
        self._dialog_styles = dict()
        self._name = ''

    def load(self, filename):
        with open(filename, 'r') as f:
            tmp = json.load(f)
            self._name = tmp['name']
            self._prompt_styles = tmp['prompt']
            self._dialog_styles = tmp['dialog']

    def for_prompt(self):
        return merge_styles([
            default_ui_style(),
            Style(list(self._prompt_styles.items()))
        ])
    def for_dialog(self):
        return merge_styles([
            default_ui_style(),
            Style(list(self._dialog_styles.items()))
        ])

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump({
                'name': self._name,
                'prompt': self._prompt_styles,
                'dialog': self._dialog_styles
            }, f, indent=2)



class ThemeRegistry(object):

    def __init__(self):
        self._themes = {}
        self._current_theme = 'default'

    def register(self, alias, theme):
        assert isinstance(theme, Theme)
        if alias in self._themes:
            raise AlreadyRegisteredError(
                'theme {} already registered'.format(alias))
        self._themes[alias] = theme


    def set_current(self, alias):
        if alias not in self._themes:
            raise ThemeNotFoundError('theme {} not registered'.format(alias))
        self._current_theme = alias

    def get_current(self):
        return self._themes[self._current_theme]


_registry = ThemeRegistry()


def register(alias, theme):
    _registry.register(alias, theme)

def for_dialog():
    return _registry.get_current().for_dialog()

def for_prompt():
    return _registry.get_current().for_prompt()

def set_theme(alias):
    _registry.set_current(alias)
