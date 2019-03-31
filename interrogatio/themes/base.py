import abc
import json
import six

from prompt_toolkit.styles import Style, default_ui_style, merge_styles

from ..core.constants import InputMode
from ..core.styles import to_style_token

from ..core.registries import get_input_handlers_registry

__all__ = [
    'Theme',
    'DefaultTheme',
    # 'PurpleTheme',
    'get_theme_manager'
]


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


class Theme:

    def __init__(self):
        self._styles = dict()

    def load(self, filename):
        with open(filename, 'r') as f:
            self._styles = json.load(f)
    
    def to_style(self):
        return merge_styles([
            default_ui_style(),
            Style(list(self._styles.items()))
        ])

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self._styles, f, indent=2)
        

class DefaultTheme(Theme):
    def __init__(self):
        self._styles = {
            'dialog': to_style_token(bg='#4444ff'),
            'dialog.body': to_style_token(fg='#000000', bg='#ffffff'),
            'dialog frame.label': to_style_token(fg='magenta', attr='bold'),
            'dialog shadow': to_style_token(bg='#000088'),
            'dialog.body shadow': to_style_token(bg='#aaaaaa'),
            
            'button': to_style_token(),
            'button.arrow': to_style_token(attr='bold'),
            'button.focused': to_style_token(fg='#ffffff', bg='#aa0000'),
            
            'prompt.error': to_style_token(fg='red', attr='bold underline'),
            'dialog.error': to_style_token(fg='red', attr='bold'),
            
            'prompt.input.question': to_style_token(fg='darkblue'),
            'prompt.input.answer': to_style_token(fg='orange', attr='bold'),
            'dialog.input.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'dialog.input.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),
            
            'prompt.password.question': to_style_token(fg='darkblue'),
            'prompt.password.answer': to_style_token(fg='orange', attr='bold'),
            'dialog.password.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'dialog.password.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'prompt.path.question': to_style_token(fg='darkblue'),
            'prompt.path.answer': to_style_token(fg='orange', attr='bold'),
            'dialog.path.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'dialog.path.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),
            
            'prompt.repassword.question': to_style_token(fg='darkblue'),
            'prompt.repassword.answer': to_style_token(fg='orange', attr='bold'),
            'dialog.repassword.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'dialog.repassword.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'prompt.text.question': to_style_token(fg='darkblue'),
            'prompt.text.answer': to_style_token(fg='orange', attr='bold'),
            'dialog.text.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'dialog.text.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),


            'prompt.selectone.question': to_style_token(fg='darkblue'),
            'prompt.selectone.answer': to_style_token(fg='darkblue', attr='bold'),
            'prompt.selectone.answer radio': to_style_token(fg='darkblue', attr='bold'),
            'prompt.selectone.answer radio-selected': to_style_token(fg='cyan'),
            'prompt.selectone.answer radio-checked': to_style_token(fg='orange', attr='bold'),

            'dialog.selectone.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'dialog.selectone.answer': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'dialog.selectone.answer radio': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'dialog.selectone.answer radio-selected': to_style_token(fg='cyan', bg='#eeeeee'),
            'dialog.selectone.answer radio-checked': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'prompt.selectmany.question': to_style_token(fg='darkblue'),
            'prompt.selectmany.answer': to_style_token(fg='darkblue', attr='bold'),
            'prompt.selectmany.answer checkbox': to_style_token(fg='darkblue', attr='bold'),
            'prompt.selectmany.answer checkbox-selected': to_style_token(fg='cyan'),
            'prompt.selectmany.answer checkbox-checked': to_style_token(fg='orange', attr='bold'),

            'dialog.selectmany.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'dialog.selectmany.answer': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'dialog.selectmany.answer checkbox': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'dialog.selectmany.answer checkbox-selected': to_style_token(fg='cyan', bg='#eeeeee'),
            'dialog.selectmany.answer checkbox-checked': to_style_token(fg='orange', bg='#eeeeee', attr='bold')
        }
