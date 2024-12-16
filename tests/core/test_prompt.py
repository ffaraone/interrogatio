from datetime import UTC, datetime

import pytest

from interrogatio.core.exceptions import InvalidQuestionError
from interrogatio.core.prompt import interrogatio


def test_string_handler(mock_input):
    questions = [
        {
            "name": "question",
            "type": "input",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text("this is the answer\n")
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "this is the answer"


def test_string_handler_ctrl_c(mock_input):
    questions = [
        {
            "name": "question",
            "type": "input",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text("\x03")
    answers = interrogatio(questions)

    assert answers is None


def test_string_handler_invalid(mocker, mock_input):
    questions = [
        {
            "name": "question",
            "type": "input",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    mocked_style = mocker.MagicMock()
    mocker.patch(
        "interrogatio.core.prompt.for_prompt",
        return_value=mocked_style,
    )
    mocked_text = mocker.MagicMock()
    mocked_formatted_text = mocker.patch(
        "interrogatio.core.prompt.FormattedText",
        return_value=mocked_text,
    )
    mocked_print = mocker.patch("interrogatio.core.prompt.print_formatted_text")
    mock_input.send_text("\n\x03")
    interrogatio(questions)

    mocked_print.assert_called_once_with(
        mocked_text,
        style=mocked_style,
    )

    mocked_formatted_text.assert_called_once_with(
        [("class:error", "this field is required")],
    )


def test_password_handler(mock_input):
    questions = [
        {
            "name": "question",
            "type": "password",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text("mypassword\n")
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "mypassword"


def test_password_handler_ctrl_c(mock_input):
    questions = [
        {
            "name": "question",
            "type": "password",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text("\x03")
    answers = interrogatio(questions)

    assert answers is None


def test_password_handler_invalid(mocker, mock_input):
    questions = [
        {
            "name": "question",
            "type": "password",
            "message": "message",
            "description": "description",
            "validators": [{"name": "required"}],
        },
    ]
    mocked_style = mocker.MagicMock()
    mocker.patch(
        "interrogatio.core.prompt.for_prompt",
        return_value=mocked_style,
    )
    mocked_text = mocker.MagicMock()
    mocked_formatted_text = mocker.patch(
        "interrogatio.core.prompt.FormattedText",
        return_value=mocked_text,
    )
    mocked_print = mocker.patch("interrogatio.core.prompt.print_formatted_text")
    mock_input.send_text("\n\x03")
    interrogatio(questions)

    mocked_print.assert_called_once_with(
        mocked_text,
        style=mocked_style,
    )

    mocked_formatted_text.assert_called_once_with(
        [("class:error", "this field is required")],
    )


def test_selectone_handler(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\x1b[B " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "second"


def test_selectone_handler_up(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\x1b[B\x1b[A " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "first"


def test_selectone_handler_page_down(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\x1b[6~ " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "third"


def test_selectone_handler_page_up(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\x1b[6~\x1b[5~ " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "first"


def test_selectone_handler_value_initial(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("T " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "third"


def test_selectone_handler_value_initial_not_found(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("Z " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "first"


def test_selectone_handler_with_default(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
            "default": "third",
        },
    ]

    mock_input.send_text(chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == "third"


def test_selectone_handler_ctrl_c(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectone",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\x03")
    answers = interrogatio(questions)

    assert answers is None


def test_selectmany_handler(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\t\t \x1b[B " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert sorted(answers["question"]) == sorted(["first", "second"])


def test_selectmany_handler_with_checked(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
            "default": {"first", "third"},
        },
    ]

    mock_input.send_text("\t\t" + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert sorted(answers["question"]) == sorted(["first", "third"])


def test_selectmany_handler_check_uncheck(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\t\t  " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == []


def test_selectmany_handler_up(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\t\t \x1b[B \x1b[A " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == ["second"]


def test_selectmany_handler_page_down(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\t\t\x1b[6~ " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == ["third"]


def test_selectmany_handler_page_up(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\t\t\x1b[6~\x1b[5~ " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == ["first"]


def test_selectmany_handler_initial(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\t\tS T " + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert sorted(answers["question"]) == sorted(["second", "third"])


def test_selectmany_handler_initial_not_found(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\t\tZ" + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == []


def test_selectmany_handler_select_all(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text(" \t\t" + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert sorted(answers["question"]) == sorted(["first", "second", "third"])


def test_selectmany_handler_select_none(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text(" \t \t" + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == []


def test_selectmany_handler_ctrl_c(mock_input):
    questions = [
        {
            "name": "question",
            "type": "selectmany",
            "message": "message",
            "description": "description",
            "values": [
                ("first", "First"),
                ("second", "Second"),
                ("third", "Third"),
            ],
        },
    ]

    mock_input.send_text("\x03")
    answers = interrogatio(questions)

    assert answers is None


def test_date_handler(mock_input):
    questions = [
        {
            "name": "question",
            "type": "date",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text("20200101" + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == datetime(
        2020,
        1,
        1,
        tzinfo=UTC,
    )


def test_date_handler_go_previous(mock_input):
    questions = [
        {
            "name": "question",
            "type": "date",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text(
        "20200101" + chr(127) + chr(127) + chr(127) + "201" + chr(13),
    )
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == datetime(
        2020,
        2,
        1,
        tzinfo=UTC,
    )


def test_date_handler_go_previous_beginning(mock_input):
    questions = [
        {
            "name": "question",
            "type": "date",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text(
        "20200101" + chr(127) * 9 + "20220706" + chr(13),
    )
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == datetime(
        2022,
        7,
        6,
        tzinfo=UTC,
    )


def test_date_handler_no_value(mock_input):
    questions = [
        {
            "name": "question",
            "type": "date",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text(chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] is None


def test_date_handler_invalid_char(mock_input):
    questions = [
        {
            "name": "question",
            "type": "date",
            "message": "message",
            "description": "description",
            "disabled": False,
        },
    ]

    mock_input.send_text("**##**@@" + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] is None


def test_date_handler_exceed_length(mock_input):
    questions = [
        {
            "name": "question",
            "type": "date",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text("2020010101" + chr(13))
    answers = interrogatio(questions)

    assert "question" in answers
    assert answers["question"] == datetime(
        2020,
        1,
        1,
        tzinfo=UTC,
    )


def test_daterange_handler(mock_input):
    questions = [
        {
            "name": "question",
            "type": "daterange",
            "message": "message",
            "description": "description",
        },
    ]

    mock_input.send_text("20200101\t20210101" + chr(13))
    answers = interrogatio(questions)
    assert "question" in answers
    assert answers["question"] == {
        "from": datetime(2020, 1, 1, tzinfo=UTC),
        "to": datetime(2021, 1, 1, tzinfo=UTC),
    }


def test_disabled_handler(mock_input):
    questions = [
        {
            "name": "question",
            "type": "input",
            "message": "message",
            "description": "description",
            "disabled": True,
        },
    ]

    mock_input.send_text("this is the answer\n")
    answers = interrogatio(questions)

    assert len(answers) == 0


def test_disabled_handler_invalid(mock_input):
    questions = [
        {
            "name": "question",
            "type": "input",
            "message": "message",
            "description": "description",
            "disabled": "not callable or boolean",
        },
    ]

    mock_input.send_text("this is the answer\n")

    with pytest.raises(InvalidQuestionError) as cv:
        interrogatio(questions)

    assert str(cv.value) == "Disabled flag must be a boolean or callable."
