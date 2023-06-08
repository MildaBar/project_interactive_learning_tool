import csv


# main login of the question-adding process
def question_mode():
    print("You chose to add questions. Let's start!\n")
    while True:
        try:
            user_input()
            if not continue_questions():
                break
        except SyntaxError:
            print("Invalid input.")
            continue


# prompt the user to enter wether they want to continue adding questions or not
def continue_questions():
    while True:
        add_questions = input("\n" + "Do you want to continue? (yes/no): ").lower()
        if add_questions == "no":
            return False
        elif add_questions == "yes":
            return True


# save questions to a csv file
def save_question_to_csv(file_path, question_type, question_text, answer):
    fieldnames = [
        "ID",
        "QUESTION",
        "ANSWER",
        "ACTIVITY",
        "Q SHOWN DURING PRACTICE",
        "WEIGHT",
        "Q SHOWN DURING TEST",
        "CORRECTLY ANSWERED Q",
    ]
    with open(file_path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()

        if isinstance(answer, list):
            answer = ", ".join(answer)
        writer.writerow(
            {
                "ID": question_type + str(count_questions(file_path) + 1),
                "QUESTION": question_text,
                "ANSWER": str(answer),
                "ACTIVITY": True,
                "Q SHOWN DURING PRACTICE": 0,
                "WEIGHT": 1.0,
                "Q SHOWN DURING TEST": 0,
                "CORRECTLY ANSWERED Q": 0,
            }
        )


class Quiz_question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = [option.strip() for option in answer]

    # call save method to save questions to csv file
    def save(self):
        save_question_to_csv("statistics.csv", "Q", self.question, self.answer)


class Free_form_question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def save(self):
        save_question_to_csv("statistics.csv", "FFT", self.question, self.answer)


# return the number of questions in the file
def count_questions(file_name):
    with open(file_name) as file:
        return sum(1 for line in file if line.startswith("Q") or line.startswith("FFT"))


# prompt the user to enter the question type
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
                while True:
                    question = input(
                        "Enter question / enter options seperated by comma: "
                    )
                    if "/" not in question or question.split("/")[1].strip() == "":
                        print("Try again. Example of the input: 'question / options').")
                    else:
                        question_type(user_question_type, question)
                        break
            elif user_question_type == "free-form text":
                question = input("Question: ")
                question_type(user_question_type, question)
                break
            break


# determine the type of question based on the user input
def question_type(user_input_question, question):
    if user_input_question == "free-form text":
        answer = input("Enter answer: ")
        free_form_question = Free_form_question(question, answer)
        free_form_question.save()

    elif user_input_question == "quiz":
        options = input("Enter correct answer from the options: ").split(",")
        quiz_question = Quiz_question(question, options)
        quiz_question.save()
