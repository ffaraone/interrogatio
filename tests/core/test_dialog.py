from interrogatio.core.dialog import dialogus, show_dialog


def test_dialogus(mocker):
    mocked_set_theme = mocker.patch('interrogatio.core.dialog.set_theme')
    mocked_show_dialog = mocker.patch('interrogatio.core.dialog.show_dialog')
    mocked_validate = mocker.patch(
        'interrogatio.core.dialog.validate_questions',
    )

    args = ([{'name': 'question1'}], 'title')
    kwargs = {
        'intro': 'intro',
        'summary': True,
        'fast_forward': False,
        'next_text': 'next_text',
        'previous_text': 'previous_text',
        'cancel_text': 'cancel_text',
        'finish_text': 'finish_text',
    }

    dialogus(*args, **kwargs)

    mocked_set_theme.assert_called_once_with('default')
    mocked_validate.assert_called_once_with(args[0])
    mocked_show_dialog.assert_called_once_with(*args, **kwargs)


def test_show_dialog(mocker):

    mocker.patch(
        'interrogatio.core.dialog.for_dialog',
        return_value='a style',
    )
    mocked_handler = mocker.MagicMock()
    mocked_handler.get_answer.return_value = {'question': 'answer'}
    mocked_handler.is_disabled.return_value = False

    mocked_disabled_handler = mocker.MagicMock()
    mocked_disabled_handler.is_disabled.return_value = True
    mocker.patch(
        'interrogatio.core.dialog.get_instance',
        side_effect=[mocked_handler, mocked_disabled_handler],
    )
    mocked_app = mocker.MagicMock()
    mocked_app.run.return_value = True

    mocked_app_cls = mocker.patch(
        'interrogatio.core.dialog.Application',
        return_value=mocked_app,
    )

    mocked_wz = mocker.MagicMock()
    mocked_wz_cls = mocker.patch(
        'interrogatio.core.dialog.WizardDialog',
        return_value=mocked_wz,
    )
    mocked_layout = mocker.MagicMock()
    mocked_layout_cls = mocker.patch(
        'interrogatio.core.dialog.Layout',
        return_value=mocked_layout,
    )

    args = ([{'name': 'question'}, {'name': 'disabled_question'}], 'title')
    kwargs = {
        'intro': 'intro',
        'summary': True,
        'fast_forward': False,
        'next_text': 'next_text',
        'previous_text': 'previous_text',
        'cancel_text': 'cancel_text',
        'finish_text': 'finish_text',
    }

    answers = show_dialog(*args, **kwargs)

    mocked_wz_cls.assert_called_once_with(
        'title',
        [mocked_handler, mocked_disabled_handler],
        **kwargs,
    )
    mocked_layout_cls.assert_called_once_with(mocked_wz)
    mocked_app_cls.assert_called_once_with(
        layout=mocked_layout,
        mouse_support=True,
        style='a style',
        full_screen=True,
    )

    assert answers == {'question': 'answer'}


def test_show_dialog_cancel(mocker):

    mocker.patch(
        'interrogatio.core.dialog.for_dialog',
    )
    mocked_handler = mocker.MagicMock()
    mocker.patch(
        'interrogatio.core.dialog.get_instance',
        return_value=mocked_handler,
    )
    mocked_app = mocker.MagicMock()
    mocked_app.run.return_value = False

    mocker.patch(
        'interrogatio.core.dialog.Application',
        return_value=mocked_app,
    )
    mocker.patch(
        'interrogatio.core.dialog.WizardDialog',
    )
    mocker.patch(
        'interrogatio.core.dialog.Layout',
    )

    args = ([{'name': 'question1'}], 'title')
    kwargs = {
        'intro': 'intro',
        'summary': True,
        'next_text': 'next_text',
        'previous_text': 'previous_text',
        'cancel_text': 'cancel_text',
        'finish_text': 'finish_text',
    }

    answers = show_dialog(*args, **kwargs)

    assert answers is None
