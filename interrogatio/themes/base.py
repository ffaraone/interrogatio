from prompt_toolkit.styles import Style, default_ui_style, merge_styles

from ..enums import Mode
from .styles import (ValueStyle, ErrorStyle, InputStyle, PasswordStyle,
                     Rule, SelectOneStyle, SelectManyStyle, DialogStyle)

__all__ = [
    'Theme',
    'DefaultTheme',
    'get_theme_manager'
]


class Theme(object):

    def __init__(self):
        self.rules = set()
        self.dialog_style = None


    def set_component_style(self, component_style):
        assert isinstance(component_style, InputStyle)
        self.rules.add(component_style)

    def set_dialog_style(self, dialog_style):
        self.dialog_style = dialog_style

    def to_style(self):
        styles = []
        for component in self.rules:
            styles.extend(component.to_style())

        if self.dialog_style:
            styles.extend(self.dialog_style.to_style())

        return merge_styles([
            default_ui_style(),
            Style(styles)
        ])
        

class DefaultTheme(Theme):
    def __init__(self):
        super(DefaultTheme, self).__init__()
        self.set_component_style(ErrorStyle(Mode.PROMPT))
        self.set_component_style(ErrorStyle(Mode.DIALOG))
        self.set_component_style(ValueStyle(Mode.PROMPT))
        self.set_component_style(ValueStyle(Mode.DIALOG))
        self.set_component_style(PasswordStyle(Mode.PROMPT))
        self.set_component_style(PasswordStyle(Mode.DIALOG))
        self.set_component_style(SelectOneStyle(Mode.PROMPT))
        self.set_component_style(SelectOneStyle(Mode.DIALOG))
        self.set_component_style(SelectManyStyle(Mode.PROMPT))
        self.set_component_style(SelectManyStyle(Mode.DIALOG))
        self.set_dialog_style(DialogStyle())


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
