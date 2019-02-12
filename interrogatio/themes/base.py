from prompt_toolkit.styles import Style, default_ui_style, merge_styles

from ..enums import Mode
from .styles import (ValueStyle, ErrorStyle, InputStyle, PasswordStyle,
                     Rule, SelectOneStyle, SelectManyStyle, DialogStyle)

from ..handlers import get_handlers_registry

__all__ = [
    'Theme',
    'DefaultTheme',
    'get_theme_manager'
]


class Theme(object):

    def __init__(self):
        self._inputs_styles = dict(prompt=dict(), dialog=dict())
        self._dialogs_style = None
        self._buttons_style = None
        self._registry = get_handlers_registry()

    def set_input_style(self, input_alias, mode, **rules):
        handler_class = self._registry[input_alias]
        self._inputs_styles[mode][input_alias] = Style(
            handler_class.get_style(mode, rules))

    def to_style(self):
        styles = [default_ui_style()]
        for mode in [Mode.PROMPT, Mode.DIALOG]:
            styles.extend([s for s in self._inputs_styles[mode].values()])
        return merge_styles(styles)
        

class DefaultTheme(Theme):
    def __init__(self):
        super(DefaultTheme, self).__init__()
        # self.set_component_style(ErrorStyle(Mode.PROMPT))
        # self.set_component_style(ErrorStyle(Mode.DIALOG))
        # self.set_component_style(ValueStyle(Mode.PROMPT))
        # self.set_component_style(ValueStyle(Mode.DIALOG))
        # self.set_component_style(PasswordStyle(Mode.PROMPT))
        # self.set_component_style(PasswordStyle(Mode.DIALOG))
        # self.set_component_style(SelectOneStyle(Mode.PROMPT))
        # self.set_component_style(SelectOneStyle(Mode.DIALOG))
        # self.set_component_style(SelectManyStyle(Mode.PROMPT))
        # self.set_component_style(SelectManyStyle(Mode.DIALOG))
        # self.set_dialog_style(DialogStyle())


class ThemeManager(object):

    def __init__(self, current_theme):
        self._current_theme = current_theme

    def set_current_theme(self, theme):
        assert isinstance(theme, Theme)
        self._current_theme = theme

    def get_current_theme(self):
        return self._current_theme

    def get_current_style(self):
        return self.get_current_theme().to_style()

manager = ThemeManager(DefaultTheme())

def get_theme_manager():
    return manager
