import csv
import os
import shutil


class DisableEnableQuestion:
    def __init__(self, file_path):
        self.file_path = file_path

    def enable_question(self, question):
        self._set_question_activity(question, True)

    def disable_question(self, question):
        self._set_question_activity(question, False)

    def _set_question_activity(self, question, activity):
        temp_file_path = self.file_path + ".temp"
        with open(self.file_path, mode="r") as file, open(
            temp_file_path, mode="w", newline=""
        ) as temp_file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if row["ID"] == question:
                    row["ACTIVITY"] = str(activity)
                writer.writerow(row)

        # Replace the original file with the temporary file
        os.remove(self.file_path)
        shutil.move(temp_file_path, self.file_path)

# user can disable or enable file
def disable_enable_mode():
    print("You chose to disable / enable questions. Let's start!\n")
    user_choice = input("What do you want to do, disable or enable question: ").lower()
    manager = DisableEnableQuestion("statistics.csv")
    while True:
        if user_choice == "disable":
            disable_question = input("Write ID of the question you want to DISABLE: ")
            if check_question_activity(disable_question) == True:
                question_text, answer = get_answer_and_question(disable_question)
                make_sure_disable = input(
                    f"Do you want to disable QUESTION: '{question_text}', with ANSWER: '{answer}'? "
                )
                if make_sure_disable.lower() == "yes":
                    manager.disable_question(disable_question)
                    print("Question disabled sucessfully.")
                    break
            else:
                print("This question is already disabled. Chose another one.")
        elif user_choice == "enable":
            enable_question = input("Write ID of the question you want to ENABLE: ")
            if check_question_activity(enable_question) == True:
                print("This question is already enabled. Chose another one.")
            else:
                question_text, answer = get_answer_and_question(enable_question)
                make_sure_enable = input(
                    f"Do you want to enable QUESTION: '{question_text}', with ANSWER: '{answer}'? "
                )
                if make_sure_enable.lower() == "yes":
                    manager.enable_question(enable_question)
                    print("Question enabled sucessfully.")
                    break


def get_answer_and_question(question_id):
    with open("statistics.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == question_id:
                question_text = row["QUESTION"]
                answer = row["ANSWER"]
                return question_text, answer
    return None, None


def check_question_activity(q_id):
    with open("statistics.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == q_id and row[3] == "True":
                return True
    return False
