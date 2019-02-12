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

class ComponentStyle(six.with_metaclass(abc.ABCMeta, object)):

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

class ErrorStyle(ComponentStyle):
    def __init__(self, mode, message=None):
        message = message or Rule(fg='darkred', attr='bold underline')
        super(ErrorStyle, self).__init__(mode, message=message)
        self._message = message

    def to_style(self):
        return [('{}.error'.format(self._mode), str(self._message))]    

class InputStyle(ComponentStyle):

    def __init__(self, mode, question=None, answer=None):
        if mode == Mode.PROMPT:
            question = question or Rule(fg='darkblue')
            answer = answer or Rule(fg='orange', attr='bold')
        else:
            question = question or Rule(fg='darkblue', bg='#eeeeee')
            answer = answer or Rule(fg='orange', bg='#eeeeee', attr='bold')            
        super(InputStyle, self).__init__(mode, 
                                         question=question,
                                         answer=answer)

        self._question = question
        self._answer = answer

    def to_style(self):     
        return [
            ('{}.input.question'.format(self._mode), str(self._question)),
            ('{}.input.answer'.format(self._mode), str(self._answer))
        ]   



class PasswordStyle(ComponentStyle):
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


class SelectOneStyle(ComponentStyle):

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


class SelectManyStyle(ComponentStyle):

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
