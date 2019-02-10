from prompt_toolkit.styles import (ANSI_COLOR_NAMES,
                                   Style, default_ui_style, merge_styles)
from prompt_toolkit.styles.named_colors import NAMED_COLORS

__all__ = [
    'Rule',
    'Theme',
    'DefaultTheme',
    'get_theme_manager'
]

ATTRIBUTES = [
    'bold',
    'underline',
    'italic',
    'blink',
    'reverse',
    'hidden'
]

ANSI_COLOR_NAMES_ALIASES = {
    'ansidarkgray': 'ansibrightblack',
    'ansiteal': 'ansicyan',
    'ansiturquoise': 'ansibrightcyan',
    'ansibrown': 'ansiyellow',
    'ansipurple': 'ansimagenta',
    'ansifuchsia': 'ansibrightmagenta',
    'ansilightgray': 'ansigray',
    'ansidarkred': 'ansired',
    'ansidarkgreen': 'ansigreen',
    'ansidarkblue': 'ansiblue',
}

class Rule:

    INPUT_PROMPT_QUESTION = 'interrogatio.question'
    INPUT_PROMPT_ERROR = 'interrogatio.error'
    INPUT_PROMPT_ANSWER = ''
    INPUT_DIALOG_QUESTION = 'label'
    INPUT_DIALOG_ANSWER = 'dialog.body text-area'
    INPUT_DIALOG_LASTLINE = 'dialog.body text-area last-line'
    SELECTONE_PROMPT_QUESTION = 'radio'
    SELECTONE_PROMPT_SELECTED = 'radio-selected'
    SELECTONE_PROMPT_CHECKED = 'radio-checked'
    SELECTONE_DIALOG_QUESTION = 'dialog.body radio'
    SELECTONE_DIALOG_SELECTED = 'dialog.body radio-selected'
    SELECTONE_DIALOG_CHECKED = 'dialog.body radio-checked'



class Theme(object):

    def __init__(self):
        self.rules = {}

    
    def set_rule(self, name, fg=None, bg=None, attr=None):
        self.rules[name] = (fg, bg, attr)


    def to_style(self):
        rules = [] 
        for name, info in self.rules.items():
            fg, bg, attr = info
            rule = []
            if bg:
                rule.append('bg:{}'.format(bg))
            if fg:
                rule.append(fg)
            if isinstance(attr, str):
                rule.append(attr)
            elif isinstance(attr, (list, tuple)):
                rule.extend(attr)
            rules.append((name, ' '.join(rule)))
        return merge_styles([
            default_ui_style(),
            Style(rules)
        ])
        

class DefaultTheme(Theme):
    def __init__(self):
        super(DefaultTheme, self).__init__()


        self.set_rule(Rule.INPUT_PROMPT_QUESTION, fg='#efa147')
        self.set_rule(Rule.INPUT_PROMPT_ANSWER, fg='ansiblue')
        self.set_rule(Rule.INPUT_PROMPT_ERROR, fg='ansired')
        self.set_rule(Rule.SELECTONE_PROMPT_QUESTION, fg='#efa147')
        self.set_rule(Rule.SELECTONE_PROMPT_CHECKED, fg='ansiblue')
        self.set_rule(Rule.SELECTONE_PROMPT_SELECTED, fg='ansigreen')
        self.set_rule(Rule.INPUT_DIALOG_QUESTION, fg='#efa147')
        self.set_rule(Rule.INPUT_DIALOG_ANSWER, fg='ansiblue')
        self.set_rule(Rule.SELECTONE_DIALOG_QUESTION, fg='#efa147')
        self.set_rule(Rule.SELECTONE_DIALOG_CHECKED, fg='ansiblue')
        self.set_rule(Rule.SELECTONE_DIALOG_SELECTED, fg='ansigreen')

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