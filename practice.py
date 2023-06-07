import csv
import difflib


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
        self.question_weights = (
            {}
        )  # create the 'question_weights' attribute as an empty dictionary
        self._load_question_counts_from_csv()

    def run_quiz(self):
        active_questions = self._get_active_questions()
        self._load_weights_from_csv()

        question_pool = []

        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            header = rows[0]
            for row in rows[1:]:
                question_id = row[0]
                if question_id in active_questions:
                    question_pool.append(row)

            question_pool.sort(key=lambda row: self.question_weights.get(row[0], 1.0))

            for row in question_pool:
                question_id = row[0]
                if row[0].startswith("FFT"):
                    self._run_fft_question(row)
                else:
                    self._run_multiple_choice_question(row)
                # Update the question counts in the CSV rows
                question = row[1]
                count = self.get_question_count(question)
                row[4] = str(count)

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        self._save_weights_to_csv()
        self._save_counts_to_csv()

    def _run_fft_question(self, row):
        qu_id = row[0]
        question = row[1]
        answer = row[2]
        self._increment_question_count(row[1])

        print(question)
        user_answer = input("YOUR ANSWER: ")
        if (
            difflib.SequenceMatcher(None, user_answer.lower(), answer.lower()).ratio()
            >= 0.9
        ):
            print("Correct")
            self._update_question_weight(qu_id, decrease=True, weight_index=5)
        else:
            print(f"Incorrect. The correct answer is: '{answer}'")
            self._update_question_weight(qu_id, decrease=False, weight_index=5)

    def _run_multiple_choice_question(self, row):
        qu_id = row[0]
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
                self._update_question_weight(qu_id, decrease=True, weight_index=5)
            else:
                print(f"Incorrect. The correct answer is: '{answer}'")
                self._update_question_weight(qu_id, decrease=False, weight_index=5)

    def _load_weights_from_csv(self):
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                question_id = row[0]
                weight = float(row[5])
                self.question_weights[question_id] = weight

    def _update_question_weight(self, qu_id, decrease, weight_index):
        # Update the weight in memory
        weight = self.question_weights[qu_id]
        if decrease:
            weight *= 0.9  # Decrease the weight by 10%
        else:
            weight *= 1.1  # Increase the weight by 10%
        self.question_weights[qu_id] = weight

        # format the weight as a float number
        formatted_weight = round(weight, 2)

        # Update the weight in the CSV file
        with open(self.filename, "r") as file:
            rows = list(csv.reader(file))
            for row in rows:
                if row[0] == qu_id:
                    row[weight_index] = formatted_weight
                    break

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def _save_weights_to_csv(self):
        with open(self.filename, "r") as file:
            rows = list(csv.reader(file))
            for row in rows[1:]:
                question_id = row[0]
                weight = self.question_weights.get(question_id, 1.0)
                row[5] = round(weight, 2)

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

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

    def _load_question_counts_from_csv(self):
        with open(self.filename, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                question = row[1]
                count = int(row[4])
                self.question_counts[question] = count

    def _save_counts_to_csv(self):
        with open(self.filename, "r") as file:
            rows = list(csv.reader(file))
            for row in rows[1:]:
                question = row[1]
                count = self.get_question_count(question)
                row[4] = str(count)

        with open(self.filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)


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
