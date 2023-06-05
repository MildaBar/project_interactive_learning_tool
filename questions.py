import csv
from disable_enable import DisableEnableQuestion


class Question:
    def __init__(self, question):
        self.question = question

    # The parent class has an empty save method that is overridden by the child classes to save the question and answer to a file.
    def save(self):
        pass


def save_question_to_csv(file_path, question_type, question_text, answer):
    fieldnames = [
        "ID",
        "QUESTION",
        "ANSWER",
        "ACTIVITY",
        "Q SHOWN DURING PRACTICE",
        "WEIGHT OF Q PRACTICE",
        "Q SHOWN DURING TEST",
        "CORRECTLY ANSWERED Q",
    ]
    with open(file_path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()  # Write headers only if the file is empty
        writer.writerow(
            {
                "ID": question_type + str(count_questions(file_path) + 1),
                "QUESTION": question_text,
                "ANSWER": str(answer),
                "ACTIVITY": True,
                "Q SHOWN DURING PRACTICE": 0,
                "WEIGHT OF Q PRACTICE": 1.0
            }
        )


class Quiz_question(Question):
    def __init__(self, question, answer):
        super().__init__(question)
        self.answer = [option.strip() for option in answer]

    def save(self):
        save_question_to_csv("statistics.csv", "Q", self.question, self.answer)


class Free_form_question(Question):
    def __init__(self, question, answer):
        super().__init__(question)
        self.answer = answer

    def save(self):
        save_question_to_csv("statistics.csv", "FFT", self.question, self.answer)


def count_questions(file_name):
    with open(file_name) as file:
        return sum(1 for line in file if line.startswith("Q") or line.startswith("FFT"))


def question_mode():
    print("You chose to add questions. Let's start!\n")
    while True:
        user_input()
        if input("\n" + "Do you want to continue? (yes/no): ").lower() == "no":
            count_user_questions = count_questions("statistics.csv")
            if count_user_questions < 5:
                print(
                    f"You need at least 5 questions! You have {count_user_questions} questions"
                )
                continue
            else:
                break


def user_input():
    while True:
        try:
            user_question_type = input(
                "Enter question type ('free-form text' or 'quiz'): "
            )
            if user_question_type not in ["free-form text", "quiz"]:
                raise ValueError("Invalid question type")
        except ValueError as e:
            print(e)
            continue
        else:
            if user_question_type == "quiz":
                question = input("Enter question / enter options seperated by comma: ")
                question_type(user_question_type, question)
                break
            elif user_question_type == "free-form text":
                question = input("Question: ")
                question_type(user_question_type, question)
                break

def question_type(user_input_question, question):
    if user_input_question == "free-form text":
        answer = input("Enter answer: ")
        free_form_question = Free_form_question(question, answer)
        free_form_question.save()

    elif user_input_question == "quiz":
        options = input("Enter correct answer from the options: ").split(",")
        quiz_question = Quiz_question(question, options)
        quiz_question.save()
