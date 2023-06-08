from questions import question_mode
from disable_enable import disable_enable_mode
from practice import practice
from test_mode import test_mode
from statistics_mode import statistics_mode


def main():
    options = [
        "Add questions mode",
        "Statistics viewing mode",
        "Disable / enable question mode",
        "Practice mode",
        "Test mode",
    ]

    print("Hello! This is a list of modes:")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    user_input = input(
        "What mode do you want to choose? Write the number of a choice: "
    )
    user_choice = options[int(user_input) - 1]
    mode_choice(user_choice)

def mode_choice(user_choice):
    try:
        match user_choice:
            case "Add questions mode":
                question_mode()
            case "Statistics viewing mode":
                statistics_mode()
            case "Disable / enable question mode":
                disable_enable_mode()
            case "Practice mode":
                practice()
            case "Test mode":
                test_mode()
            case _:
                print("Invalid mode")
    except FileNotFoundError:
        print("No CSV file found. Please choose another mode.")


if __name__ == "__main__":
    main()
