import csv
import difflib
import pandas as pd

# 1. ask questions from csv file

class Quiz:
    def __init__(self, filename):
        self.filename = filename
        self.question_counts = {}

    def run_quiz(self):
        self._load_question_counts()

        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            header = rows[0]
            for row in rows[1:]:
                if row[0].startswith('FFT'):
                    self._run_fft_question(row)
                else:
                    self._run_multiple_choice_question(row)

        # Update the question counts in the CSV rows
        for row in rows[1:]:
            question = row[1]
            count = self.get_question_count(question)
            row[4] = str(count)

        with open(self.filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def _run_fft_question(self, row):
        question = row[1]
        answer = row[2]
        self._increment_question_count(question)

        print(question)
        user_answer = input("YOUR ANSWER: ")
        if difflib.SequenceMatcher(None, user_answer.lower(), answer.lower()).ratio() >= 0.9:
            print("Correct")
        else:
            print(f"Incorrect. The correct answer is {answer}")

    def _run_multiple_choice_question(self, row):
        question, options = row[1].split(" / ")
        answer = row[2]
        self._increment_question_count(row[1])

        print(question)
        print(f'Options: {options}')
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

    def _load_question_counts(self):
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                question = row[1]
                count = int(row[4])
                self.question_counts[question] = count

# Example usage:
def practice():
    print("\n" + "You choce to a practice questions. Let's start!")
    quiz = Quiz("statistics.csv")
    quiz.run_quiz()
    


# 2. in statistics file create a statistic about answered questions
# df = pd.read_csv("statistics.csv")

# correctly_answered = df["CORRECTLY ANSWERED Q"].sum()
# total_questions = len(df)

# 3. from statistic depend how questions will be given

# 4. do not show questions that are disabled