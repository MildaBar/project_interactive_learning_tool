from questions import question_mode
from disable_enable import disable_enable_mode
from practice import practice
import csv


def main():
    options = [
        "Add questions mode",
        "Statistics viewing mode",
        "Disable / enable question mode",
        "Practice mode",
        "Test mode",
        "Select profile",
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
    match user_choice:
        case "Add questions mode":
            question_mode()
        case "Statistics viewing mode":
            pass
        case "Disable / enable question mode":
            disable_enable_mode()
        case "Practice mode":
            practice()
        case "Test mode":
            pass
        case "Select profile":
            pass
        case _:
            print("Invalid mode")

if __name__ == "__main__":
    main()
