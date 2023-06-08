from questions import question_mode
from disable_enable import disable_enable_mode
from practice import practice
from test_mode import test_mode
from statistics_mode import statistics_mode


def main():
    options = [
        "Add questions",
        "Statistics",
        "Disable / enable questions",
        "Practice questions",
        "Test",
    ]

    print("Hello! This is a list of modes:")
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    while True:
        user_input = input("What mode do you want to choose? Write the number of your choice: ")
        try:
            user_choice = options[int(user_input) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number.")

    mode_choice(user_choice)


def mode_choice(user_choice):
    try:
        match user_choice:
            case "Add questions":
                question_mode()
            case "Statistics":
                statistics_mode()
            case "Disable / enable questions":
                disable_enable_mode()
            case "Practice questions":
                practice()
            case "Test":
                test_mode()
            case _:
                print("Invalid mode")
    except FileNotFoundError:
        print("No CSV file found. Please choose another mode.")


if __name__ == "__main__":
    main()
