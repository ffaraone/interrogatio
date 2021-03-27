import pytest

from interrogatio.shortcuts import dialogs


@pytest.mark.parametrize(
    ('func', 'kwargs', 'expected_kwargs'),
    (
        (
            dialogs.yes_no_dialog,
            {
                'title': 'title',
                'text': 'text',
                'yes_text': 'yes_text',
                'no_text': 'no_text',
            },
            {
                'title': 'title',
                'text': 'text',
                'yes_text': 'yes_text',
                'no_text': 'no_text',
            },
        ),
        (
            dialogs.button_dialog,
            {
                'title': 'title',
                'text': 'text',
            },
            {
                'title': 'title',
                'text': 'text',
                'buttons': [],
            },
        ),
        (
            dialogs.button_dialog,
            {
                'title': 'title',
                'text': 'text',
                'buttons': ['btn1', 'btn2'],
            },
            {
                'title': 'title',
                'text': 'text',
                'buttons': ['btn1', 'btn2'],
            },
        ),
        (
            dialogs.input_dialog,
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
            },
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
                'completer': None,
                'password': False,
            },
        ),
        (
            dialogs.input_dialog,
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
                'completer': 'completer',
                'password': True,
            },
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
                'completer': 'completer',
                'password': True,
            },
        ),
        (
            dialogs.message_dialog,
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
            },
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
            },
        ),
        (
            dialogs.radiolist_dialog,
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
            },
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
                'values': None,
            },
        ),
        (
            dialogs.radiolist_dialog,
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
                'values': ['a', 'b'],
            },
            {
                'title': 'title',
                'text': 'text',
                'ok_text': 'ok_text',
                'cancel_text': 'cancel_text',
                'values': ['a', 'b'],
            },
        ),
        (
            dialogs.progress_dialog,
            {
                'title': 'title',
                'text': 'text',
            },
            {
                'title': 'title',
                'text': 'text',
                'run_callback': None,
            },
        ),
        (
            dialogs.progress_dialog,
            {
                'title': 'title',
                'text': 'text',
                'run_callback': 'a function',
            },
            {
                'title': 'title',
                'text': 'text',
                'run_callback': 'a function',
            },
        ),
    ),
)
def test_dialogs(mocker, func, kwargs, expected_kwargs):
    mocked = mocker.patch(
        f'interrogatio.shortcuts.dialogs.pt_{func.__name__}',
    )
    mocker.patch(
        'interrogatio.shortcuts.dialogs.for_dialog',
        return_value='a style',
    )

    func(**kwargs)

    assert mocked.mock_calls[0].kwargs == {
        **expected_kwargs,
        'style': 'a style',
    }

    kwargs['style'] = 'another style'

    func(**kwargs)

    assert mocked.mock_calls[1].kwargs == {
        **expected_kwargs,
        'style': 'another style',
    }
