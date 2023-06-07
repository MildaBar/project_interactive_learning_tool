from questions import count_questions
import datetime
import random
import difflib
import csv


# SELECT THE NR OF QUESTIONS FOR THE TEST WHICH IS NOT LARGER THAN THE TOTAL NUMBER OF QUESTIONS ADDED
def test_mode():
    count_user_questions = count_questions("statistics.csv")
    if count_user_questions < 5:
        print(
            f"You need at least 5 questions! You have {count_user_questions} questions"
        )
        return
    else:
        print("\n" + "You chose to a practice questions. Let's start!")
        print("\n" + "You chose to have a test! Let's start!")
        check_question()


def check_question():
    filename = "statistics.csv"
    # total_questions = count_questions(filename)
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
        # check the error
        except SyntaxError:
            print("Invalid input. Please enter a valid number of questions.")


# THE QUESTIONS ARE CHOSEN FULLY RANDOMLY AND DEPEND OF DISABLE/ENABLE
# EACH QUESTION CAN ONLY APPEAR ONCE AT THE MOST IN THE TEST
# AT THE END OF THE QUESTIONS, THE USER IS SHOWS SCORE


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


class Questionnaire:
    def __init__(self, filename):
        self.filename = filename
        self.answered_questions = 0
        self.total_questions = 0
        self.asked_questions = []
        self.score_recorder = ScoreRecorder("results.txt")

    def choose_question(self, question_id):
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == question_id:
                    if row[0].startswith("FFT"):
                        self._run_fft_question(row)
                    else:
                        self._run_multiple_choice_question(row)

    def _run_fft_question(self, row):
        qu_id = row[0]
        question = row[1]
        answer = row[2]

        if question in self.asked_questions:
            return

        print(question)
        user_answer = input("YOUR ANSWER: ")
        if (
            difflib.SequenceMatcher(None, user_answer.lower(), answer.lower()).ratio()
            >= 0.9
        ):
            print("Correct")
            self.answered_questions += 1
            self.increment_correct_questions(qu_id)
        else:
            print(f"Incorrect. The correct answer is {answer}")
        self.total_questions += 1
        self.asked_questions.append(question)
        self.increment_question_asked(qu_id)

    def _run_multiple_choice_question(self, row):
        qu_id = row[0]
        question, options = row[1].split(" / ")
        answer = eval(row[2])

        # if the questions is already present in the self.asked_questions list, the question has been asked before. Code executes the return statement, which skips the current iteration of the loop and moves to the next question
        if question in self.asked_questions:
            return

        print(question)
        print(f"Options: {options}")
        user_answer = input("YOUR ANSWER: ")
        if user_answer in answer:
            print(f"Correct.")
            self.answered_questions += 1
            self.increment_correct_questions(qu_id)
        else:
            print(f"Incorrect. The correct answer is {answer}")
        self.total_questions += 1
        self.asked_questions.append(question)
        self.increment_question_asked(qu_id)

    def increment_correct_questions(self, question_id):
        # open csv file and read its data
        with open("statistics.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)

        column_index = 7

        # update value in the CSV file
        for row in data:
            if row[0] == question_id:
                row[column_index] = str(int(row[column_index]) + 1)

        # write updated data back to csv file
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
        print(f"\nScore: {score}%")


# THE LIST OF SCORES SHOULD BE SAVED IN A SEPERATE results.txt FILE - THE DATE AND TIME SHOULD BE ADDED NEXT TO THE SCORE AS WEL
class ScoreRecorder:
    def __init__(self, filename):
        self.filename = filename

    def record_score(self, score):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, "a") as file:
            file.write(f"Date: {current_date}\n")
            file.write(f"Score: {score}%\n\n")
