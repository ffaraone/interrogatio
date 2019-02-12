import abc
import six


from collections import namedtuple

from ...enums import Mode

class Rule:
    def __init__(self, fg='', bg='', attr=''):
        self.fg = fg
        self.bg = bg
        self.attr = attr

    def __str__(self):
        tokens = []
        if self.bg:
            tokens.append('bg:{}'.format(self.bg))
        if self.fg:
            tokens.append(self.fg)
        if self.attr:
            tokens.append(self.attr)
        return ' '.join(tokens)

class InputStyle(six.with_metaclass(abc.ABCMeta, object)):

    def __init__(self, mode, **kwargs):
        assert mode in [Mode.PROMPT,  Mode.DIALOG]
        self._mode = mode
        for arg in kwargs.values():
            assert isinstance(arg, Rule)

    @abc.abstractmethod
    def to_style(self):
        pass

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash('{}.{}'.format(self._mode, self.__class__))

class ErrorStyle(InputStyle):
    def __init__(self, mode, message=None):
        if mode == Mode.PROMPT:
            message = message or Rule(fg='darkred', attr='bold underline')
        else:
            message = message or Rule(fg='darkred', bg='#eeeeee', 
                                      attr='bold')
        super(ErrorStyle, self).__init__(mode, message=message)
        self._message = message

    def to_style(self):
        return [('{}.error'.format(self._mode), str(self._message))]    

class DialogStyle(object):
    def __init__(self, dialog=None, label=None, body=None, shadow=None):
        self._dialog = dialog or Rule(bg='#4444ff')
        self._label = label or Rule(fg='magenta', attr='bold')
        self._body = body or Rule(fg='#000000', bg='#ffffff')
        self._shadow = shadow or Rule(bg='#00aa00')
    
    def to_style(self):
        return [
            ('dialog', str(self._dialog)),
            ('dialog.body', str(self._body)),
            ('dialog frame.label', str(self._label)),
            ('dialog shadow', str(self._shadow))
    ]    

class ValueStyle(InputStyle):

    def __init__(self, mode, question=None, answer=None):
        if mode == Mode.PROMPT:
            question = question or Rule(fg='darkblue')
            answer = answer or Rule(fg='orange', attr='bold')
        else:
            question = question or Rule(fg='darkblue', bg='#eeeeee')
            answer = answer or Rule(fg='orange', bg='#eeeeee', attr='bold')            
        super(ValueStyle, self).__init__(mode, 
                                         question=question,
                                         answer=answer)

        self._question = question
        self._answer = answer

    def to_style(self):     
        return [
            ('{}.input.question'.format(self._mode), str(self._question)),
            ('{}.input.answer'.format(self._mode), str(self._answer))
        ]   



class PasswordStyle(InputStyle):
    def __init__(self, mode, question=None, answer=None):

        if mode == Mode.PROMPT:
            question = question or Rule(fg='darkblue')
            answer = answer or Rule(fg='orange', attr='bold')
        else:
            question = question or Rule(fg='darkblue', bg='#eeeeee')
            answer = answer or Rule(fg='orange', bg='#eeeeee', attr='bold')
        super(PasswordStyle, self).__init__(mode, 
                                         question=question,
                                         answer=answer)

        self._question = question
        self._answer = answer

    def to_style(self):
        return [
            ('{}.password.question'.format(self._mode), str(self._question)),
            ('{}.password.answer'.format(self._mode), str(self._answer)),
        ]


class SelectOneStyle(InputStyle):

    def __init__(self, mode, question=None, answer=None,
                 selected=None, checked=None):

        if mode == Mode.PROMPT:
            question = question or Rule(fg='darkblue')
            answer = answer or Rule(fg='darkblue', attr='bold')
            selected = selected or Rule(fg='cyan')
            checked = checked or Rule(fg='orange', attr='bold')
        else:
            question = question or Rule(fg='darkblue', bg='#eeeeee')
            answer = answer or Rule(fg='darkblue', bg='#eeeeee', attr='bold')
            selected = selected or Rule(fg='cyan', bg='#eeeeee')
            checked = checked or Rule(fg='orange', bg='#eeeeee', attr='bold')
                
        super(SelectOneStyle, self).__init__(
            mode,
            question=question,
            answer=answer,
            selected=selected,
            checked=checked
        )
        self._question = question
        self._answer = answer
        self._selected = selected
        self._checked = checked


    def to_style(self):
        return [
            ('{}.selectone.question'.format(self._mode), str(self._question)),
            ('{}.selectone.answer'.format(self._mode), str(self._answer)),
            ('{}.selectone.answer radio'.format(self._mode), str(self._answer)),
            ('{}.selectone.answer radio-selected'.format(self._mode), 
             str(self._selected)),
            ('{}.selectone.answer radio-checked'.format(self._mode), 
             str(self._checked))
        ]


class SelectManyStyle(InputStyle):

    def __init__(self, mode, question=None, answer=None,
                 selected=None, checked=None):

        if mode == Mode.PROMPT:
            question = question or Rule(fg='darkblue')
            answer = answer or Rule(fg='darkblue', attr='bold')
            selected = selected or Rule(fg='cyan')
            checked = checked or Rule(fg='orange', attr='bold')
        else:
            question = question or Rule(fg='darkblue', bg='#eeeeee')
            answer = answer or Rule(fg='darkblue', bg='#eeeeee', attr='bold')
            selected = selected or Rule(fg='cyan', bg='#eeeeee')
            checked = checked or Rule(fg='orange', bg='#eeeeee', attr='bold')

        super(SelectManyStyle, self).__init__(
            mode,
            question=question,
            answer=answer,
            selected=selected,
            checked=checked
        )
        self._question = question
        self._answer = answer
        self._selected = selected
        self._checked = checked


    def to_style(self):
        return [
            ('{}.selectmany.question'.format(self._mode), str(self._question)),
            ('{}.selectmany.answer'.format(self._mode), str(self._answer)),
            ('{}.selectmany.answer checkbox'.format(self._mode), str(self._answer)),
            ('{}.selectmany.answer checkbox-selected'.format(self._mode), 
             str(self._selected)),
            ('{}.selectmany.answer checkbox-checked'.format(self._mode), 
             str(self._checked))
        ]
