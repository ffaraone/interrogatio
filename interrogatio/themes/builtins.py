import os
from .base import Theme, register
from .utils import to_style_token

class DefaultTheme(Theme):
    def __init__(self):
        self.load(os.path.join(
            os.path.dirname(__file__),
            'theme_files',
            'default.json'
        ))
        # self._name = 'default'
        # self._prompt_styles = {
        #     'error': to_style_token(fg='red', attr='bold underline'),
        #     'input.question': to_style_token(fg='darkblue'),
        #     'input.answer': to_style_token(fg='orange', attr='bold'),

            
        #     'password.question': to_style_token(fg='darkblue'),
        #     'password.answer': to_style_token(fg='orange', attr='bold'),

        #     'path.question': to_style_token(fg='darkblue'),
        #     'path.answer': to_style_token(fg='orange', attr='bold'),
            
        #     'repassword.question': to_style_token(fg='darkblue'),
        #     'repassword.answer': to_style_token(fg='orange', attr='bold'),

        #     'text.question': to_style_token(fg='darkblue'),
        #     'text.answer': to_style_token(fg='orange', attr='bold'),
    
        #     'selectone.question': to_style_token(fg='darkblue'),
        #     'selectone.answer': to_style_token(fg='darkblue', attr='bold'),
        #     'selectone.answer radio': to_style_token(fg='darkblue', attr='bold'),
        #     'selectone.answer radio-selected': to_style_token(fg='cyan'),
        #     'selectone.answer radio-checked': to_style_token(fg='orange', attr='bold'),

        #     'selectmany.question': to_style_token(fg='darkblue'),
        #     'selectmany.answer': to_style_token(fg='darkblue', attr='bold'),
        #     'selectmany.answer checkbox': to_style_token(fg='darkblue', attr='bold'),
        #     'selectmany.answer checkbox-selected': to_style_token(fg='cyan'),
        #     'selectmany.answer checkbox-checked': to_style_token(fg='orange', attr='bold'),


        # }

        # self._dialog_styles = {
        #     'dialog': to_style_token(bg='#4444ff'),
        #     'dialog.body': to_style_token(fg='#000000', bg='#ffffff'),
        #     'dialog frame.label': to_style_token(fg='magenta', attr='bold'),
        #     'dialog shadow': to_style_token(bg='#000088'),
        #     'dialog.body shadow': to_style_token(bg='#aaaaaa'),
            
        #     'button': to_style_token(),
        #     'button.arrow': to_style_token(attr='bold'),
        #     'button.focused': to_style_token(fg='#ffffff', bg='#aa0000'),

        #     'error': to_style_token(fg='red', attr='bold'),

        #     'input.question': to_style_token(fg='darkblue', bg='#eeeeee'),
        #     'input.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),
    
        #     'password.question': to_style_token(fg='darkblue', bg='#eeeeee'),
        #     'password.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

        #     'path.question': to_style_token(fg='darkblue', bg='#eeeeee'),
        #     'path.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

        #     'repassword.question': to_style_token(fg='darkblue', bg='#eeeeee'),
        #     'repassword.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

        #     'text.question': to_style_token(fg='darkblue', bg='#eeeeee'),
        #     'text.answer': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

        #     'selectone.question': to_style_token(fg='darkblue', bg='#eeeeee'),
        #     'selectone.answer': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
        #     'selectone.answer radio': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
        #     'selectone.answer radio-selected': to_style_token(fg='cyan', bg='#eeeeee'),
        #     'selectone.answer radio-checked': to_style_token(fg='orange', bg='#eeeeee', attr='bold'),

        #     'selectmany.question': to_style_token(fg='darkblue', bg='#eeeeee'),
        #     'selectmany.answer': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
        #     'selectmany.answer checkbox': to_style_token(fg='darkblue', bg='#eeeeee', attr='bold'),
        #     'selectmany.answer checkbox-selected': to_style_token(fg='cyan', bg='#eeeeee'),
        #     'selectmany.answer checkbox-checked': to_style_token(fg='orange', bg='#eeeeee', attr='bold')
        # }

register('default', DefaultTheme())


class PurpleTheme(Theme):
    def __init__(self):
        self.load(os.path.join(
            os.path.dirname(__file__),
            'theme_files',
            'purple.json'
        ))

register('purple', PurpleTheme())