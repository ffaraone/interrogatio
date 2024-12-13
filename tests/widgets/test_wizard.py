from interrogatio.handlers import QHandler, get_instance
from interrogatio.validators import RequiredValidator
from interrogatio.widgets.wizard import WizardDialog


def test_wizard_init_default():
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
            "disabled": True,
        },
        {
            "name": "question3",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    assert len(wz.steps) == 3


def test_wizard_init_intro_summary():
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers, intro="intro", summary=True)
    assert len(wz.steps) == 4


def test_wizard_get_title():
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    assert wz.get_title() == "title - 1 of 2"


def test_wizard_get_steps_label():
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question3",
            "type": "input",
            "message": "message",
            "description": "description",
            "disabled": True,
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    steps_lables = wz.get_steps_labels()
    class_current = steps_lables.children[0].content.text[0][0]
    assert "class:dialog.step.current " == class_current
    assert "1. Question1" == steps_lables.children[0].content.text[0][1]
    assert "class:dialog.step " == steps_lables.children[1].content.text[0][0]
    assert "2. Question2" == steps_lables.children[1].content.text[0][1]
    assert "disabled" in steps_lables.children[2].content.text[0][0]
    assert "3. Question3" == steps_lables.children[2].content.text[0][1]


def test_wizard_get_status():
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    assert wz.get_status().text == ""

    wz.error_messages = "An error"
    assert wz.get_status().content.text[0][0] == "class:error"
    assert wz.get_status().content.text[0][1] == "An error"


def test_wizard_cancel(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    wz.cancel()
    mocked_app.exit.assert_called_once_with(result=False)


def test_wizard_next(mocker):
    def always_true(context):
        return True

    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
            "disabled": always_true,
        },
        {
            "name": "question3",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
            "disabled": False,
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocked_validate = mocker.patch.object(WizardDialog, "validate")
    wz = WizardDialog("title", handlers)
    wz.next()  # noqa: B305
    assert wz.current_step_idx == 2
    assert wz.current_step == wz.steps[2]
    assert len(wz.buttons) == 3
    assert wz.previous_btn in wz.buttons
    assert wz.next_btn.text == wz.label_finish
    assert mocked_validate.call_count == 2


def test_wizard_next_with_disabled(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question3",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
            "disabled": True,
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocked_validate = mocker.patch.object(WizardDialog, "validate")
    wz = WizardDialog("title", handlers)
    wz.next()  # noqa: B305
    assert wz.current_step_idx == 1
    assert wz.current_step == wz.steps[1]
    assert len(wz.buttons) == 3
    assert wz.previous_btn in wz.buttons
    assert wz.next_btn.text == wz.label_finish
    mocked_validate.assert_called_once()


def test_wizard_previous(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
            "disabled": True,
        },
        {
            "name": "question3",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question4",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocker.patch.object(WizardDialog, "validate")
    wz = WizardDialog("title", handlers)
    wz.next()  # noqa: B305
    wz.previous()
    assert wz.current_step_idx == 0
    assert wz.current_step == wz.steps[0]
    assert len(wz.buttons) == 2
    assert wz.previous_btn not in wz.buttons


def test_wizard_next_latest_step(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocked_validate = mocker.patch.object(WizardDialog, "validate")
    wz = WizardDialog("title", handlers)
    wz.next()  # noqa: B305
    wz.next()  # noqa: B305
    assert wz.current_step_idx == 1
    assert wz.current_step == wz.steps[1]
    assert len(wz.buttons) == 3
    assert wz.previous_btn in wz.buttons
    assert mocked_validate.call_count == 2
    mocked_app.exit.assert_called_once_with(result=True)


def test_wizard_previous_first_step(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocker.patch.object(WizardDialog, "validate")
    wz = WizardDialog("title", handlers)
    wz.next()  # noqa: B305
    wz.previous()
    wz.previous()
    assert wz.current_step_idx == 0
    assert wz.current_step == wz.steps[0]
    assert len(wz.buttons) == 2
    assert wz.previous_btn not in wz.buttons


def test_wizard_next_latest_step_with_summary(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocked_validate = mocker.patch.object(WizardDialog, "validate")
    wz = WizardDialog("title", handlers, summary=True)
    wz.next()  # noqa: B305
    wz.next()  # noqa: B305
    wz.next()  # noqa: B305
    assert wz.current_step_idx == 2
    assert wz.current_step == wz.steps[2]
    assert len(wz.buttons) == 3
    assert wz.previous_btn in wz.buttons
    assert mocked_validate.call_count == 3
    mocked_app.exit.assert_called_once_with(result=True)


def test_get_summary(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocker.patch.object(
        QHandler,
        "get_formatted_value",
        side_effect=["value1", "value2"],
    )

    wz = WizardDialog("title", handlers, summary=True)
    summary = wz.get_summary()
    expected_text1 = summary.content.text[0][1] + summary.content.text[1][1]
    expected_text2 = summary.content.text[2][1] + summary.content.text[3][1]
    assert "Question1: value1" in expected_text1
    assert "Question2: value2" in expected_text2


def test_single_step(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    wz.next()  # noqa: B305
    assert wz.current_step_idx == 0
    assert wz.current_step == wz.steps[0]
    assert len(wz.buttons) == 2
    assert wz.previous_btn not in wz.buttons
    mocked_app.exit.assert_called_once_with(result=True)


def test_wizard_next_validate_invalid(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [RequiredValidator("This field is required")],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    wz.next()  # noqa: B305
    assert wz.current_step_idx == 0
    assert wz.current_step == wz.steps[0]
    assert len(wz.buttons) == 2
    assert wz.error_messages == "This field is required"


def test_wizard_get_current_step_container(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    assert wz.get_current_step_container() == wz.steps[0]["layout"]


def test_wizard_get_buttons_container(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
        },
    ]
    handlers = [get_instance(q) for q in questions]
    wz = WizardDialog("title", handlers)
    assert wz.get_buttons_container() is not None


def test_wizard_fast_forward(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "default": "value",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
            "disabled": True,
        },
        {
            "name": "question3",
            "type": "input",
            "message": "message",
            "description": "description",
            "default": "value",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocker.patch.object(WizardDialog, "validate")
    wz = WizardDialog("title", handlers, fast_forward=True)
    assert wz.current_step_idx == 2
    assert wz.current_step == wz.steps[-1]


def test_wizard_fast_forward_with_error(mocker):
    mocked_app = mocker.MagicMock()
    mocker.patch("interrogatio.widgets.wizard.get_app", return_value=mocked_app)
    questions = [
        {
            "name": "question1",
            "type": "input",
            "message": "message",
            "description": "description",
            "default": "value",
            "validators": [{"name": "required"}],
        },
        {
            "name": "question2",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
            "disabled": True,
        },
        {
            "name": "question3",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    handlers = [get_instance(q) for q in questions]
    mocker.patch.object(
        WizardDialog,
        "validate",
        side_effect=[True, True, False],
    )
    wz = WizardDialog("title", handlers, summary=True, fast_forward=True)
    assert wz.current_step_idx == 2
    assert wz.current_step == wz.steps[2]
