from questions import count_questions
import datetime
import random
import difflib
import csv


# run test mode program
def test_mode():
    count_user_questions = count_questions("statistics.csv")
    if count_user_questions < 5:
        print(
            f"You need at least 5 questions! You have {count_user_questions} questions"
        )
        return
    else:
        print("\n" + "You chose to have a test! Let's start!")
        check_question()


# prompt the user to enter the number of questions for the test
def check_question():
    filename = "statistics.csv"
    while True:
        try:
            question_num = int(input("Select number of questions for the test: "))
            if question_num <= 0:
                print("Number of questions must be greater than zero. Try again.")
            elif question_num > count_questions(filename):
                print(
                    "Selected number of questions is larger than the total number of questions adeded. Try again."
                )
            else:
                check_question_activity(filename, question_num)
                break
        except SyntaxError:
            print("Invalid input. Please enter a valid number of questions.")


# find questions that are active
def check_question_activity(filename, num_questions):
    with open("statistics.csv", "r") as file:
        reader = csv.reader(file)
        questions = []
        for row in reader:
            question_id = row[0]
            activity = row[3]
            if activity == "True":
                questions.append(question_id)

        if len(questions) < num_questions:
            print(
                "The number of available questions is less than the requested number."
            )
            return

        selected_questions = random.sample(questions, num_questions)
        random.shuffle(selected_questions)

        questionnaire = Questionnaire(filename)
        for question_id in selected_questions:
            questionnaire.choose_question(question_id)
        questionnaire.print_score()


# manage the overall questionnaire and its statistics
class Questionnaire:
    def __init__(self, filename):
        self.filename = filename
        self.answered_questions = 0
        self.total_questions = 0
        self.asked_questions = []
        self.score_recorder = ResultRecorder("results.txt")

    def choose_question(self, question_id):
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == question_id:
                    if row[0].startswith("FFT"):
                        fft_question = FFTQuestion(row)
                        fft_question.run_question(self)
                    else:
                        mc_question = MultipleChoiceQuestion(row)
                        mc_question.run_question(self)

    def increment_correct_questions(self, question_id):
        with open("statistics.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)

        column_index = 7

        for row in data:
            if row[0] == question_id:
                row[column_index] = str(int(row[column_index]) + 1)

        with open("statistics.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def increment_question_asked(self, question_id):
        with open("statistics.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)

        column_index = 6

        for row in data:
            if row[0] == question_id:
                row[column_index] = str(int(row[column_index]) + 1)

        with open("statistics.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def print_score(self):
        score = (self.answered_questions / self.total_questions) * 100
        self.score_recorder.record_score(score)
        rounded_score = round(score, 2)  # Round the score
        formatted_score = "{:.2f}".format(rounded_score)
        print(f"\nScore: {formatted_score}%")


# free-form text question
class FFTQuestion:
    def __init__(self, row):
        self.question_id = row[0]
        self.question = row[1]
        self.answer = row[2]

    def run_question(self, questionnaire):
        if self.question in questionnaire.asked_questions:
            return

        print(self.question)
        user_answer = input("YOUR ANSWER: ")
        if (
            difflib.SequenceMatcher(
                None, user_answer.lower(), self.answer.lower()
            ).ratio()
            >= 0.6
        ):
            print("Correct")
            questionnaire.answered_questions += 1
            questionnaire.increment_correct_questions(self.question_id)
        else:
            print(f"Incorrect. The correct answer is {self.answer}")
        questionnaire.total_questions += 1
        questionnaire.asked_questions.append(self.question)
        questionnaire.increment_question_asked(self.question_id)


class MultipleChoiceQuestion:
    def __init__(self, row):
        self.question_id = row[0]
        self.question, options = row[1].split(" / ")
        self.options = options.split(",")  # Store options as a list
        self.answer = row[2]

    def run_question(self, questionnaire):
        if self.question in questionnaire.asked_questions:
            return

        print(self.question)
        print(f"Options: {', '.join(self.options)}")
        user_answer = input("YOUR ANSWER: ")
        if user_answer.lower() == self.answer.lower():
            print(f"Correct.")
            questionnaire.answered_questions += 1
            questionnaire.increment_correct_questions(self.question_id)
        else:
            print(f"Incorrect. The correct answer is {self.answer}")
        questionnaire.total_questions += 1
        questionnaire.asked_questions.append(self.question)
        questionnaire.increment_question_asked(self.question_id)


class ResultRecorder:
    def __init__(self, filename):
        self.filename = filename

    def record_score(self, score):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rounded_score = round(score, 2)  # Round the score
        formatted_score = "{:.2f}".format(rounded_score)
        with open(self.filename, "a") as file:
            file.write(f"Date: {current_date}\n")
            file.write(f"Score: {formatted_score}%\n\n")
