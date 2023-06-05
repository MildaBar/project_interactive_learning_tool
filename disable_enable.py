import csv
import os
import shutil

# Users should be able to write the ID of the question they want to disable or enable.


class DisableEnableQuestion:
    def __init__(self, file_path):
        self.file_path = file_path

        if not os.path.isfile(self.file_path):
            with open(self.file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "ID",
                        "QUESTION",
                        "ANSWER",
                        "ACTIVITY",
                        "SHOWN DURING PRACTICE",
                        "WEIGHT",
                    ]
                )

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

    def add_question(self, question):
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([question, True])


def disable_enable_mode():
    print("You chose to disable / enable questions. Let's start!\n")
    user_choice = input("What do you want to do, disable or enable question: ").lower()
    manager = DisableEnableQuestion("statistics.csv")
    while True:
        if user_choice == "disable":
            disable_question = input("Write ID of the question you want to DISABLE: ")
            make_sure_disable = input("You really want to disable this question? ")
            if make_sure_disable.lower() == "yes":
                manager.disable_question(disable_question)
                print("Question disabled sucessfully.")
                break
        elif user_choice == "enable":
            enable_question = input("Write ID of the question you want to ENABLE: ")
            make_sure_enable = input("You really want to enable this question? ")
            if make_sure_enable.lower() == "yes":
                manager.enable_question(enable_question)
                print("Question enabled sucessfully.")
                break
