import pytest

from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, VSplit, Window
from prompt_toolkit.widgets import TextArea

from interrogatio.handlers.builtins import (
    DateHandler,
    DateRangeHandler,
    MaskedInputHandler,
    PasswordHandler,
    SelectManyHandler,
    SelectOneHandler,
    StringHandler,
)
from interrogatio.widgets import DateRange, MaskedInput, SelectMany, SelectOne


@pytest.mark.parametrize(
    ('handler', 'expected_widget'),
    (
        (StringHandler, TextArea),
        (PasswordHandler, TextArea),
        (SelectOneHandler, SelectOne),
        (SelectManyHandler, SelectMany),
        (MaskedInputHandler, MaskedInput),
        (DateHandler, MaskedInput),
        (DateRangeHandler, DateRange),
    ),
)
def test_handler_get_widget_class(handler, expected_widget):
    s = handler({})
    assert issubclass(s.get_widget_class(), expected_widget)


@pytest.mark.parametrize(
    ('handler', 'expected_widget'),
    (
        (StringHandler, TextArea),
        (PasswordHandler, TextArea),
    ),
)
def test_handler_get_widget(handler, expected_widget):
    question = {}
    s = handler(question)
    assert isinstance(s.get_widget(), expected_widget)


@pytest.mark.parametrize(
    'handler',
    (
        StringHandler,
        PasswordHandler,
    ),
)
def test_textarea_handler_get_layout_cursor_position(mocker, handler):
    question = {}
    s = handler(question)
    widget = s.get_widget()
    widget.text = 'this is the text'
    s.get_layout()
    assert widget.buffer.cursor_position == len(widget.text)


@pytest.mark.parametrize(
    'handler',
    (
        StringHandler,
        PasswordHandler,
    ),
)
def test_textarea_handler_get_layout(mocker, handler):
    question = {}
    s = handler(question)
    widget = s.get_widget()
    widget.text = 'This is the widget text'
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 1
    assert layout.padding == 1
    assert isinstance(layout.children[0], VSplit)
    assert len(layout.children[0].children) == 1
    assert layout.children[0].padding == 1
    input_ctrl = layout.children[0].children[0]
    assert isinstance(input_ctrl, Window)
    assert input_ctrl.content.buffer.text == 'This is the widget text'


@pytest.mark.parametrize(
    'handler',
    (
        StringHandler,
        PasswordHandler,
    ),
)
def test_textarea_handler_get_layout_with_msg(mocker, handler):
    question = {'message': 'this is a message'}
    s = handler(question)
    widget = s.get_widget()
    widget.text = 'This is the widget text'
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 1
    assert layout.padding == 1
    assert isinstance(layout.children[0], VSplit)
    assert len(layout.children[0].children) == 2
    assert layout.children[0].padding == 1
    label_ctrl = layout.children[0].children[0]
    assert isinstance(label_ctrl, Window)
    assert label_ctrl.content.text() == 'this is a message'
    input_ctrl = layout.children[0].children[1]
    assert input_ctrl.content.buffer.text == 'This is the widget text'


@pytest.mark.parametrize(
    'handler',
    (
        StringHandler,
        PasswordHandler,
    ),
)
def test_textarea_handler_get_layout_with_description(mocker, handler):
    question = {'description': 'this is a description'}
    s = handler(question)
    widget = s.get_widget()
    widget.text = 'This is the widget text'
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 2
    assert layout.padding == 1
    label_ctrl = layout.children[0]
    assert isinstance(label_ctrl, Window)
    assert label_ctrl.content.text() == 'this is a description'

    assert isinstance(layout.children[1], VSplit)
    assert len(layout.children[1].children) == 1
    assert layout.children[1].padding == 1
    input_ctrl = layout.children[1].children[0]
    assert input_ctrl.content.buffer.text == 'This is the widget text'


@pytest.mark.parametrize(
    'handler',
    (
        StringHandler,
        PasswordHandler,
    ),
)
def test_textarea_handler_get_keybindings(handler):
    s = handler({})
    kb = s.get_keybindings()
    assert isinstance(kb, KeyBindings)
    assert kb.get_bindings_for_keys(Keys.ControlC) is not None
    assert kb.get_bindings_for_keys(Keys.Enter) is not None


@pytest.mark.parametrize(
    'handler',
    (
        StringHandler,
        PasswordHandler,
    ),
)
def test_textarea_handler_get_value(mocker, handler):
    s = handler({})
    widget_mock = mocker.MagicMock()
    widget_mock.text = 'Test text'
    s.get_widget = mocker.MagicMock(return_value=widget_mock)

    assert s.get_value() == 'Test text'


@pytest.mark.parametrize(
    ('question', 'expected'),
    (
        (
            {'default': 'default_text'},
            {
                'multiline': False,
                'text': 'default_text',
                'style': 'class:input.answer',
            },
        ),
        (
            {'multiline': True},
            {'multiline': True, 'style': 'class:input.answer'},
        ),
    ),
)
def test_string_handler_get_widget_init_kwargs(question, expected):
    s = StringHandler(question)
    assert s.get_widget_init_kwargs() == expected


@pytest.mark.parametrize(
    ('question', 'expected'),
    (
        (
            {'default': 'default_text'},
            {
                'text': 'default_text',
                'style': 'class:password.answer',
                'password': True,
                'multiline': False,
            },
        ),
        (
            {},
            {
                'multiline': False,
                'style': 'class:password.answer',
                'password': True,
            },
        ),
    ),
)
def test_password_handler_get_widget_init_kwargs(question, expected):
    s = PasswordHandler(question)
    assert s.get_widget_init_kwargs() == expected


def test_selectone_handler_get_layout(mocker):
    question = {'values': [('a', 'A')]}
    s = SelectOneHandler(question)
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 1
    assert layout.padding == 1
    assert isinstance(layout.children[0], VSplit)
    assert len(layout.children[0].children) == 1
    assert layout.children[0].padding == 1
    input_ctrl = layout.children[0].children[0]
    assert isinstance(input_ctrl, Window)


def test_selectone_handler_get_layout_with_msg(mocker):
    question = {'message': 'this is a message', 'values': [('a', 'A')]}
    s = SelectOneHandler(question)
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 1
    assert layout.padding == 1
    assert isinstance(layout.children[0], VSplit)
    assert len(layout.children[0].children) == 2
    assert layout.children[0].padding == 1
    label_ctrl = layout.children[0].children[0]
    assert isinstance(label_ctrl, Window)
    assert label_ctrl.content.text() == 'this is a message'
    input_ctrl = layout.children[0].children[1]
    assert isinstance(input_ctrl, Window)


def test_selectone_handler_get_layout_with_description(mocker):
    question = {'description': 'this is a description', 'values': [('a', 'A')]}
    s = SelectOneHandler(question)
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 2
    assert layout.padding == 1
    label_ctrl = layout.children[0]
    assert isinstance(label_ctrl, Window)
    assert label_ctrl.content.text() == 'this is a description'

    assert isinstance(layout.children[1], VSplit)
    assert len(layout.children[1].children) == 1
    assert layout.children[1].padding == 1
    input_ctrl = layout.children[1].children[0]
    assert isinstance(input_ctrl, Window)


@pytest.mark.parametrize(
    ('question', 'expected'),
    (
        (
            {'default': 'default_value', 'values': [('a', 'A')]},
            {
                'style': 'class:selectone.answer',
                'values': [('a', 'A')],
                'default': 'default_value',
            },
        ),
        (
            {'values': [('a', 'A')]},
            {
                'style': 'class:selectone.answer',
                'values': [('a', 'A')],
            },
        ),
    ),
)
def test_selectone_handler_get_widget_init_kwargs(question, expected):
    s = SelectOneHandler(question)
    assert s.get_widget_init_kwargs() == expected


def test_selectone_handler_get_keybindings():
    s = SelectOneHandler({'values': [('a', 'A')]})
    kb = s.get_keybindings()
    assert isinstance(kb, KeyBindings)
    assert kb.get_bindings_for_keys(Keys.ControlC) is not None


def test_selectone_handler_get_value(mocker):
    s = SelectOneHandler({})
    widget_mock = mocker.MagicMock()
    widget_mock.current_value = 'Test text'
    s.get_widget = mocker.MagicMock(return_value=widget_mock)
    assert s.get_value() == 'Test text'


def test_selectmany_handler_get_layout(mocker):
    question = {'values': [('a', 'A')]}
    s = SelectManyHandler(question)
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 2
    assert layout.padding == 1
    assert isinstance(layout.children[1], VSplit)
    assert len(layout.children[1].children) == 1
    assert layout.children[1].padding == 1
    input_ctrl = layout.children[1].children[0]
    assert isinstance(input_ctrl, Window)


def test_selectmany_handler_get_layout_with_msg(mocker):
    question = {'message': 'this is a message', 'values': [('a', 'A')]}
    s = SelectManyHandler(question)
    widget = s.get_widget()
    widget.text = 'This is the widget text'
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 2
    assert layout.padding == 1
    assert isinstance(layout.children[1], VSplit)
    assert len(layout.children[1].children) == 2
    assert layout.children[1].padding == 1
    label_ctrl = layout.children[1].children[0]
    assert isinstance(label_ctrl, Window)
    assert label_ctrl.content.text() == 'this is a message'
    input_ctrl = layout.children[1].children[1]
    assert isinstance(input_ctrl, Window)


def test_selectmany_handler_get_layout_with_description(mocker):
    question = {'description': 'this is a description', 'values': [('a', 'A')]}
    s = SelectOneHandler(question)
    widget = s.get_widget()
    widget.text = 'This is the widget text'
    layout = s.get_layout()
    assert isinstance(layout, HSplit)
    assert len(layout.children) == 2
    assert layout.padding == 1
    label_ctrl = layout.children[0]
    assert isinstance(label_ctrl, Window)
    assert label_ctrl.content.text() == 'this is a description'

    assert isinstance(layout.children[1], VSplit)
    assert len(layout.children[1].children) == 1
    assert layout.children[1].padding == 1
    input_ctrl = layout.children[1].children[0]
    assert isinstance(input_ctrl, Window)


@pytest.mark.parametrize(
    ('question', 'expected'),
    (
        (
            {
                'checked': ['a'],
                'default': 'default_value',
                'values': [('a', 'A')],
            },
            {
                'checked': set(['a']),
                'style': 'class:selectmany.answer',
                'values': [('a', 'A')],
                'default': 'default_value',

            },
        ),
        (
            {'values': [('a', 'A')]},
            {
                'style': 'class:selectmany.answer',
                'values': [('a', 'A')],
            },
        ),
    ),
)
def test_selectmany_handler_get_widget_init_kwargs(question, expected):
    s = SelectManyHandler(question)
    assert s.get_widget_init_kwargs() == expected


def test_selectmany_handler_get_keybindings():
    s = SelectManyHandler({'values': [('a', 'A')]})
    kb = s.get_keybindings()
    assert isinstance(kb, KeyBindings)
    assert kb.get_bindings_for_keys(Keys.ControlC) is not None


def test_selectmany_handler_get_value(mocker):
    s = SelectManyHandler({})
    widget_mock = mocker.MagicMock()
    widget_mock.checked = ['a']
    s.get_widget = mocker.MagicMock(return_value=widget_mock)
    assert s.get_value() == ['a']
