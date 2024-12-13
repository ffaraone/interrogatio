from interrogatio.validators import RequiredValidator


def test_qhandler_errors(test_handler):
    t = test_handler({})
    t._errors = ["a", "b", "c"]
    assert t.errors == ["a", "b", "c"]


def test_qhandler_get_init_extra_args(test_handler):
    t = test_handler({"extra_args": {"a": 0, "b": "1"}})
    assert t.get_init_extra_args() == {"a": 0, "b": "1"}


def test_qhandler_get_answer(mocker, test_handler):
    t = test_handler({"name": "test_field"})
    t.get_value = mocker.MagicMock(return_value="test_value")
    assert t.get_answer() == {"test_field": "test_value"}


def test_qhandler_get_variable_name(test_handler):
    t = test_handler({"name": "test_field"})
    assert t.get_variable_name() == "test_field"


def test_qhandler_is_valid_valid(mocker, test_handler):
    t = test_handler(
        {
            "name": "test_field",
            "validators": [RequiredValidator()],
        }
    )
    t.get_value = mocker.MagicMock(return_value="value")
    assert t.is_valid() is True


def test_qhandler_is_valid_invalid(mocker, test_handler):
    t = test_handler(
        {
            "name": "test_field",
            "validators": [RequiredValidator()],
        }
    )
    t.get_value = mocker.MagicMock(return_value="")
    assert t.is_valid() is False
