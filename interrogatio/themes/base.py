from prompt_toolkit.styles import Style, default_ui_style, merge_styles

from ..enums import Mode
from .styles import (ComponentStyle, ErrorStyle, InputStyle, PasswordStyle,
                     Rule, SelectOneStyle, SelectManyStyle)

__all__ = [
    'Theme',
    'DefaultTheme',
    'get_theme_manager'
]


class Theme(object):

    def __init__(self):
        self.rules = set()

    
    def set_component_style(self, component_style):
        assert isinstance(component_style, ComponentStyle)
        self.rules.add(component_style)

    def to_style(self):
        styles = []
        for component in self.rules:
            styles.extend(component.to_style())
        
        return merge_styles([
            default_ui_style(),
            Style(styles)
        ])
        

class DefaultTheme(Theme):
    def __init__(self):
        super(DefaultTheme, self).__init__()
        self.set_component_style(ErrorStyle(Mode.PROMPT))
        self.set_component_style(ErrorStyle(Mode.DIALOG))
        self.set_component_style(InputStyle(Mode.PROMPT))
        self.set_component_style(InputStyle(
            Mode.DIALOG,
            question=Rule(fg='ansiblue', bg='#eeeeee'),
            answer=Rule(fg='#efa147', bg='#eeeeee')))
        self.set_component_style(PasswordStyle(Mode.PROMPT))
        self.set_component_style(PasswordStyle  (
            Mode.DIALOG,
            question=Rule(fg='ansiblue', bg='#eeeeee'),
            answer=Rule(fg='#efa147', bg='#eeeeee')))
        self.set_component_style(SelectOneStyle(Mode.PROMPT))
        self.set_component_style(SelectOneStyle(Mode.DIALOG))
        self.set_component_style(SelectManyStyle(Mode.PROMPT))
        self.set_component_style(SelectManyStyle(Mode.DIALOG))


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
