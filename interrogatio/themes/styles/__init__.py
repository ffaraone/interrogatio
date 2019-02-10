import abc
import six


class ComponentStyle(six.with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def to_style(self):
        pass


class InputStyle(ComponentStyle):

    def __init__(self,
        mode,
        question_fg='ansiblue',
        question_bg='',
        question_attr='',
        answer_fg='#efa147',
        answer_bg='',
        answer_attr=''):

        self._mode = mode

        self._question_fg = question_fg
        self._question_bg = question_bg
        self._question_attr = question_attr

        self._answer_fg = answer_fg
        self._answer_bg = answer_bg
        self._answer_attr = answer_attr

    def to_style(self):
        rules = []
        
        rules.append(
            (
                'label {}.input.question'.format(self._mode), 
                '{} {} {}'.format(
                    self._question_bg or 'default',
                    self._question_fg or '',
                    self._question_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'text-area {}.input.answer'.format(self._mode), 
                'bg:{} {} {}'.format(
                    self._answer_bg or 'default',
                    self._answer_fg or '',
                    self._answer_attr or ''
                ).strip()
            )
        )
        return rules


class PasswordStyle(ComponentStyle):
    def __init__(self,
        mode,
        question_fg='ansimagenta',
        question_bg='',
        question_attr='',
        answer_fg='#efa147',
        answer_bg='',
        answer_attr=''):

        self._mode = mode
        self._question_fg = question_fg
        self._question_bg = question_bg
        self._question_attr = question_attr

        self._answer_fg = answer_fg
        self._answer_bg = answer_bg
        self._answer_attr = answer_attr


    def to_style(self):
        rules = []
        
        rules.append(
            (
                'label {}.password.question'.format(self._mode), 
                '{} {} {}'.format(
                    self._question_bg or 'default',
                    self._question_fg or '',
                    self._question_attr or ''
                ).strip()
            )
        )

        rules.append(
            (
                'text-area {}.password.answer'.format(self._mode), 
                'bg:{} {} {}'.format(
                    self._answer_bg or 'default',
                    self._answer_fg or '',
                    self._answer_attr or ''
                ).strip()
            )
        )

        return rules


class SelectOneStyle(ComponentStyle):

    def __init__(self,
        mode,
        question_fg='ansiblue',
        question_bg='',
        question_attr='',
        answer_fg='#efa147',
        answer_bg='',
        answer_attr='',
        selected_answer_fg='#efa147',
        selected_answer_bg='',
        selected_answer_attr='',
        checked_answer_fg='#efa147',
        checked_answer_bg='',
        checked_answer_attr=''):

        self._mode = mode

        self._question_fg = question_fg
        self._question_bg = question_bg
        self._question_attr = question_attr

        self._answer_fg = answer_fg
        self._answer_bg = answer_bg
        self._answer_attr = answer_attr

        self._selected_answer_fg = selected_answer_fg
        self._selected_answer_bg = selected_answer_bg
        self._selected_answer_attr = selected_answer_attr

        self._checked_answer_fg = checked_answer_fg
        self._checked_answer_bg = checked_answer_bg
        self._checked_answer_attr = checked_answer_attr


    def to_style(self):
        pass
        # rules = []
        
        # rules.append(
        #     (
        #         'radio', 
        #         'bg:{} {} {}'.format(
        #             self.question_bg or 'default',
        #             self.question_fg or '',
        #             self.question_attr or ''
        #         ).strip()
        #     )
        # )

        # rules.append(
        #     (
        #         'radio-selected', 
        #         'bg:{} {} {}'.format(
        #             self.answer_bg or 'default',
        #             self.answer_fg or '',
        #             self.answer_attr or ''
        #         ).strip()
        #     )
        # )

        # rules.append(
        #     (
        #         'radio-checked', 
        #         'bg:{} {} {}'.format(
        #             self.checked_answer_bg or 'default',
        #             self.checked_answer_fg or '',
        #             self.checked_answer_attr or ''
        #         ).strip()
        #     )
        # )
        # rules.append(
        #     (
        #         'interrogatio.error', 
        #         'bg:{} {} {}'.format(
        #             self.error_bg or 'default',
        #             self.error_fg or '',
        #             self.error_attr or ''
        #         ).strip()
        #     )
        # )
        # return rules