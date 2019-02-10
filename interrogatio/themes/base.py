import abc
import six

from prompt_toolkit.styles import (ANSI_COLOR_NAMES,
                                   Style, default_ui_style, merge_styles)
from prompt_toolkit.styles.named_colors import NAMED_COLORS

__all__ = [
    'ComponentStyle',
    'PromptInputStyle',
    'PromptPasswordStyle',
    'PromptSelectOneStyle',
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



# class Rule:

#     INPUT_PROMPT_QUESTION = 'interrogatio.question'
#     INPUT_PROMPT_ERROR = 'interrogatio.error'
#     INPUT_PROMPT_ANSWER = ''
#     INPUT_DIALOG_QUESTION = 'label'
#     INPUT_DIALOG_ANSWER = 'dialog.body text-area'
#     INPUT_DIALOG_LASTLINE = 'dialog.body text-area last-line'
#     SELECTONE_PROMPT_QUESTION = 'radio'
#     SELECTONE_PROMPT_SELECTED = 'radio-selected'
#     SELECTONE_PROMPT_CHECKED = 'radio-checked'
#     SELECTONE_DIALOG_QUESTION = 'dialog.body radio'
#     SELECTONE_DIALOG_SELECTED = 'dialog.body radio-selected'
#     SELECTONE_DIALOG_CHECKED = 'dialog.body radio-checked'



class ComponentStyle(six.with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def to_style(self):
        pass


class PromptInputStyle(ComponentStyle):

    def __init__(self,
        question_fg='ansiblue',
        question_bg='',
        question_attr='',
        answer_fg='#efa147',
        answer_bg='',
        answer_attr='',
        error_fg='ansired',
        error_bg='',
        error_attr='underline'):

        self.question_fg = question_fg
        self.question_bg = question_bg
        self.question_attr = question_attr

        self.answer_fg = answer_fg
        self.answer_bg = answer_bg
        self.answer_attr = answer_attr
        
        self.error_fg = error_fg
        self.error_bg = error_bg
        self.error_attr = error_attr


    def to_style(self):
        rules = []
        
        rules.append(
            (
                'label input.question', 
                '{} {} {}'.format(
                    self.question_bg or 'default',
                    self.question_fg or '',
                    self.question_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'text-area input.answer', 
                'bg:{} {} {}'.format(
                    self.answer_bg or 'default',
                    self.answer_fg or '',
                    self.answer_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'interrogatio.error', 
                'bg:{} {} {}'.format(
                    self.error_bg or 'default',
                    self.error_fg or '',
                    self.error_attr or ''
                ).strip()
            )
        )
        return rules


class PromptPasswordStyle(ComponentStyle):
    def __init__(self,
        question_fg='ansimagenta',
        question_bg='',
        question_attr='',
        answer_fg='#efa147',
        answer_bg='',
        answer_attr='',
        error_fg='ansired',
        error_bg='',
        error_attr='underline'):

        self.question_fg = question_fg
        self.question_bg = question_bg
        self.question_attr = question_attr

        self.answer_fg = answer_fg
        self.answer_bg = answer_bg
        self.answer_attr = answer_attr
        
        self.error_fg = error_fg
        self.error_bg = error_bg
        self.error_attr = error_attr


    def to_style(self):
        rules = []
        
        rules.append(
            (
                'label password.question', 
                '{} {} {}'.format(
                    self.question_bg or 'default',
                    self.question_fg or '',
                    self.question_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'text-area password.answer', 
                'bg:{} {} {}'.format(
                    self.answer_bg or 'default',
                    self.answer_fg or '',
                    self.answer_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'interrogatio.error', 
                'bg:{} {} {}'.format(
                    self.error_bg or 'default',
                    self.error_fg or '',
                    self.error_attr or ''
                ).strip()
            )
        )
        return rules


class PromptSelectOneStyle(ComponentStyle):

    def __init__(self,
        question_fg='ansiblue',
        question_bg='',
        question_attr='',
        answer_fg='#efa147',
        answer_bg='',
        answer_attr='',
        checked_answer_fg='#efa147',
        checked_answer_bg='',
        checked_answer_attr='',
        error_fg='ansired',
        error_bg='',
        error_attr='underline'):

        self.question_fg = question_fg
        self.question_bg = question_bg
        self.question_attr = question_attr

        self.answer_fg = answer_fg
        self.answer_bg = answer_bg
        self.answer_attr = answer_attr

        self.checked_answer_fg = checked_answer_fg
        self.checked_answer_bg = checked_answer_bg
        self.checked_answer_attr = checked_answer_attr
        
        self.error_fg = error_fg
        self.error_bg = error_bg
        self.error_attr = error_attr

    SELECTONE_PROMPT_QUESTION = 'radio'
    SELECTONE_PROMPT_SELECTED = 'radio-selected'
    SELECTONE_PROMPT_CHECKED = 'radio-checked'

    def to_style(self):
        rules = []
        
        rules.append(
            (
                'radio', 
                'bg:{} {} {}'.format(
                    self.question_bg or 'default',
                    self.question_fg or '',
                    self.question_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'radio-selected', 
                'bg:{} {} {}'.format(
                    self.answer_bg or 'default',
                    self.answer_fg or '',
                    self.answer_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'radio-checked', 
                'bg:{} {} {}'.format(
                    self.checked_answer_bg or 'default',
                    self.checked_answer_fg or '',
                    self.checked_answer_attr or ''
                ).strip()
            )
        )
        rules.append(
            (
                'interrogatio.error', 
                'bg:{} {} {}'.format(
                    self.error_bg or 'default',
                    self.error_fg or '',
                    self.error_attr or ''
                ).strip()
            )
        )
        return rules


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
        self.set_component_style(PromptInputStyle())
        self.set_component_style(PromptPasswordStyle())
        self.set_component_style(PromptSelectOneStyle())

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