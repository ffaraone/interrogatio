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

manager = ThemeManager()

def get_theme_manager():
    return manager


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
        

class DefaultTheme(Theme):
    def __init__(self):
        self._name = 'default'
        self._prompt_styles = {
            'error': to_style_token(fg='red', attr='bold underline'),
            'input.question': to_style_token(fg='darkblue'),
            'input.answer': to_style_token(fg='orange', attr='bold'),

            
            'password.question': to_style_token(fg='darkblue'),
            'password.answer': to_style_token(fg='orange', attr='bold'),

            'path.question': to_style_token(fg='darkblue'),
            'path.answer': to_style_token(fg='orange', attr='bold'),
            
            'repassword.question': to_style_token(fg='darkblue'),
            'repassword.answer': to_style_token(fg='orange', attr='bold'),

            'text.question': to_style_token(fg='darkblue'),
            'text.answer': to_style_token(fg='orange', attr='bold'),
    
            'selectone.question': to_style_token(fg='darkblue'),
            'selectone.answer': to_style_token(fg='darkblue', attr='bold'),
            'selectone.answer radio': to_style_token(fg='darkblue', attr='bold'),
            'selectone.answer radio-selected': to_style_token(fg='cyan'),
            'selectone.answer radio-checked': to_style_token(fg='orange', attr='bold'),

            'selectmany.question': to_style_token(fg='darkblue'),
            'selectmany.answer': to_style_token(fg='darkblue', attr='bold'),
            'selectmany.answer checkbox': to_style_token(fg='darkblue', attr='bold'),
            'selectmany.answer checkbox-selected': to_style_token(fg='cyan'),
            'selectmany.answer checkbox-checked': to_style_token(fg='orange', attr='bold'),


        }

        self._dialog_styles = {
            'dialog': to_style_token(bg='#4444ff'),
            'dialog.body': to_style_token(fg='#000000', bg='#ffffff'),
            'dialog frame.label': to_style_token(fg='magenta', attr='bold'),
            'dialog shadow': to_style_token(bg='#000088'),
            'dialog.body shadow': to_style_token(bg='#aaaaaa'),
            
            'button': to_style_token(),
            'button.arrow': to_style_token(attr='bold'),
            'button.focused': to_style_token(fg='#ffffff', bg='#aa0000'),

            'error': to_style_token(fg='red', attr='bold'),

            'input.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'input.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),
    
            'password.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'password.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'path.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'path.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'repassword.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'repassword.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'text.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'text.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'selectone.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'selectone.answer': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'selectone.answer radio': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'selectone.answer radio-selected': to_style_token(fg='cyan', bg='#eeeeee'),
            'selectone.answer radio-checked': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

            'selectmany.question': to_style_token(fg='darkblue', bg='#eeeeee'),
            'selectmany.answer': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'selectmany.answer checkbox': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
            'selectmany.answer checkbox-selected': to_style_token(fg='cyan', bg='#eeeeee'),
            'selectmany.answer checkbox-checked': to_style_token(fg='orange', bg='#eeeeee', attr='bold')
        }