from prompt_toolkit.styles import Style, default_ui_style, merge_styles

from ..utils.constants import InputMode
from ..utils.styles import Rule

from ..utils.registries import get_input_handlers_registry

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
        self._registry = get_input_handlers_registry()

    def set_input_style(self, input_alias, mode, **rules):
        handler_class = self._registry[input_alias]
        self._inputs_styles[mode][input_alias] = Style(
            handler_class.get_style(mode, rules))

    def to_style(self):
        styles = [default_ui_style()]
        for mode in InputMode._ALL:
            styles.extend([s for s in self._inputs_styles[mode].values()])
        return merge_styles(styles)
        

class DefaultTheme(Theme):
    def __init__(self):
        super(DefaultTheme, self).__init__()
        for mode in InputMode._ALL:
            for input_alias in self._registry:
                self.set_input_style(input_alias, mode)


class ThemeManager(object):

    def __init__(self):
        self._current_theme = None

    def set_current_theme(self, theme):
        assert isinstance(theme, Theme)
        self._current_theme = theme

    def get_current_theme(self):
        return self._current_theme

    def get_current_style(self):
        return self.get_current_theme().to_style()

manager = ThemeManager()

def get_theme_manager():
    return manager
