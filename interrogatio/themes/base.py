import abc
import six

from prompt_toolkit.styles import Style, default_ui_style, merge_styles

from ..core.constants import InputMode
from ..core.styles import Rule

from ..core.registries import get_input_handlers_registry

__all__ = [
    'Theme',
    'DefaultTheme',
    'PurpleTheme',
    'get_theme_manager'
]



class Theme(six.with_metaclass(abc.ABCMeta, object)):

    def __init__(self):
        self._inputs_styles = dict(prompt=dict(), dialog=dict())
        self._dialog_style = None
        self._button_style = None
        self._error_style = dict()
        self._registry = get_input_handlers_registry()


    @abc.abstractmethod
    def set_dialog_style(self, **rules):
        pass

    @abc.abstractmethod
    def set_button_style(self, **rules):
        pass

    @abc.abstractmethod
    def set_error_style(self, mode, **rules):
        pass

    def set_input_style(self, input_alias, mode, **rules):
        handler_class = self._registry[input_alias]
        self._inputs_styles[mode][input_alias] = Style(
            handler_class.get_style(mode, rules))

    def to_style(self):
        styles = [
            default_ui_style(), 
            self._dialog_style,
            self._button_style
        ]
        for mode in InputMode._ALL:
            styles.extend([s for s in self._inputs_styles[mode].values()])
            styles.append(self._error_style[mode])
        
        return merge_styles(styles)
        

class DefaultTheme(Theme):
    def __init__(self):
        super(DefaultTheme, self).__init__()
        for mode in InputMode._ALL:
            for input_alias in self._registry:
                self.set_input_style(input_alias, mode)
            self.set_error_style(mode)

    
    def set_dialog_style(self, **rules):
        dialog = rules.get('dialog', Rule(bg='#4444ff'))
        title = rules.get('title', Rule(fg='magenta', attr='bold'))
        body = rules.get('body', Rule(fg='#000000', bg='#ffffff'))
        shadow = rules.get('shadow', Rule(bg='#000088'))
        body_shadow = rules.get('body_shadow', Rule(bg='#aaaaaa'))

        self._dialog_style = Style([
            ('dialog', str(dialog)),
            ('dialog.body', str(body)),
            ('dialog frame.label', str(title)),
            ('dialog shadow', str(shadow)),
            ('dialog.body shadow', str(body_shadow)),
        ])

    def set_button_style(self, **rules):
        button = rules.get('button', Rule())
        arrow = rules.get('arrow', Rule(attr='bold'))
        focused = rules.get('focused', Rule(fg='#ffffff', bg='#aa0000'))
       

        self._button_style = Style([
            ('button', str(button)),
            ('button.arrow', str(arrow)),
            ('button.focused', str(focused))
        ])

    def set_error_style(self, mode, **rules):
        message = rules.get('message', Rule(fg='red', attr='bold underline'))
        if mode == InputMode.DIALOG:
            message = rules.get('message', Rule(fg='red', attr='bold'))
        self._error_style[mode] = Style([
            ('{}.error'.format(mode), str(message))
        ])


class PurpleTheme(DefaultTheme):
    def __init__(self):
        super(PurpleTheme, self).__init__()
        self.set_input_style(
            'input', 
            InputMode.DIALOG, 
            question=Rule(fg='white', bg='black', attr='bold'),
            answer=Rule(fg='magenta', bg='black', attr='bold'))

        self.set_input_style(
            'password', 
            InputMode.DIALOG, 
            question=Rule(fg='white', bg='black', attr='bold'),
            answer=Rule(fg='magenta', bg='black', attr='bold'))

        self.set_input_style(
            'selectone', 
            InputMode.DIALOG, 
            question=Rule(fg='white', bg='black', attr='bold'),
            answer=Rule(fg='white', bg='black', attr='bold'),
            checked=Rule(fg='magenta', bg='black', attr='bold'),
            selected=Rule(fg='cyan'))

        self.set_input_style(
            'selectmany', 
            InputMode.DIALOG, 
            question=Rule(fg='white', bg='black', attr='bold'),
            answer=Rule(fg='white', bg='black', attr='bold'),
            checked=Rule(fg='magenta', bg='black', attr='bold'),
            selected=Rule(fg='cyan'))


        self.set_dialog_style(
            body=Rule(bg='black', fg='white'),
            title=Rule(fg='magenta', attr='bold'),
            dialog=Rule(fg='magenta', bg='white'),
            body_shadow=Rule(bg='magenta'),
            shadow=Rule(bg='gray')
        )
        self.set_button_style(
            button=Rule(fg='white'),
            focused=Rule(bg='magenta', fg='white')
        )
        self.set_error_style(
            InputMode.DIALOG,
            message=Rule(fg='orange', bg='black', attr='bold'))


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
