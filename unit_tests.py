import pytest
from main import mode_choice


def test_user_input():
    with pytest.raises(ValueError):  # Check if a ValueError is raised
        user_question_type = "Invalid question type"  # Set the user_question_type variable to an invalid value
        if user_question_type not in [
            "free-form text",
            "quiz",
        ]:  # Check if the user_question_type is not valid
            raise ValueError(
                "Invalid question type"
            )  # Raise a ValueError if the user_question_type is not valid


def test_user_choice():
    options = [
        "Add questions",
        "Statistics",
        "Disable / enable questions",
        "Practice questions",
        "Test",
    ]

    # Simulate user input of an invalid index
    with pytest.raises(ValueError):
        user_input = "a"  # Invalid input
        user_choice = options[int(user_input) - 1]

    # Simulate user input of an out-of-bounds index
    with pytest.raises(IndexError):
        user_input = "10"  # Out-of-bounds input
        user_choice = options[int(user_input) - 1]

    # Simulate user input of a valid index
    user_input = "2"  # Valid input
    user_choice = options[int(user_input) - 1]
    assert user_choice == "Statistics"  # Assert the value of user_choice


def test_mode_choice():
    try:
        mode_choice(
            "Invalid mode"
        )  # Call the mode_choice function with an invalid mode
    except SystemExit as e:
        assert e.code == 0  # Check if the exit code is 0 (success)
        assert "Invalid mode" in str(
            e
        )  # Check if the error message contains "Invalid mode"
