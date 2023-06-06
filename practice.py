import csv
import difflib
import pandas as pd


def check_question_activity(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        questions = []
        for row in reader:
            question_id = row[0]
            activity = row[3]
            if activity == "True":
                questions.append(question_id)
        return questions


class Quiz:
    def __init__(self, filename):
        self.filename = filename
        self.question_counts = {}

    def run_quiz(self):
        active_questions = self._get_active_questions()

        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            header = rows[0]
            for row in rows[1:]:
                question_id = row[0]
                if question_id in active_questions:
                    if row[0].startswith("FFT"):
                        self._run_fft_question(row)
                    else:
                        self._run_multiple_choice_question(row)

            # Update the question counts in the CSV rows
            for row in rows[1:]:
                question = row[1]
                count = self.get_question_count(question)
                row[4] = str(count)

            with open(self.filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    def _run_fft_question(self, row):
        question = row[1]
        answer = row[2]
        self._increment_question_count(question)

        print(question)
        user_answer = input("YOUR ANSWER: ")
        if (
            difflib.SequenceMatcher(None, user_answer.lower(), answer.lower()).ratio()
            >= 0.9
        ):
            print("Correct")
        else:
            print(f"Incorrect. The correct answer is {answer}")

    def _run_multiple_choice_question(self, row):
        question_and_options = row[1].split(" / ")
        answer = row[2]
        self._increment_question_count(row[1])

        if len(question_and_options) == 2:
            question, options = question_and_options
            print(question)
            print(f"Options: {options}")
            user_answer = input("YOUR ANSWER: ")
            if user_answer in answer:
                print(f"Correct.")
            else:
                print(f"Incorrect. The correct answer is {answer}")

    def _increment_question_count(self, question):
        if question in self.question_counts:
            self.question_counts[question] += 1
        else:
            self.question_counts[question] = 1

    def get_question_count(self, question):
        return self.question_counts.get(question, 0)

    def _get_active_questions(self):
        return check_question_activity(self.filename)

    def add_question(self, question, answer):
        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["", question, answer, "", "0"])


def practice():
    questions = check_question_activity("statistics.csv")
    count_user_questions = len(questions)
    if count_user_questions < 5:
        print(
            f"You need at least 5 questions! You have {count_user_questions} questions"
        )
        return
    else:
        print("\n" + "You chose to a practice questions. Let's start!")
        quiz = Quiz("statistics.csv")
        quiz.run_quiz()
