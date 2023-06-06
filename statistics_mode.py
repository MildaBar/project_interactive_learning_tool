# The program should print out all the questions currently in the system. Each question should list:

import csv

class Statistics_view_mode:
    def __init__(self, id_num, activity, question, activity_num, correct_answers):
        self.id_num = id_num  # its unique ID number
        self.activity = activity  # whether the question is active or not
        self.question = question  # the question text
        self.activity_num = (
            activity_num  # the number of times it was shown during practice or tests
        )
        self.correct_answers = (
            correct_answers  # the percentage of times it was answered correctly
        )


statistics_info = []
# 2. in statistics file create a statistic about answered questions
# df = pd.read_csv("statistics.csv")

# correctly_answered = df["CORRECTLY ANSWERED Q"].sum()
# total_questions = len(df)
# 2. in statistics file create a statistic about answered questions
# df = pd.read_csv("statistics.csv")

# correctly_answered = df["CORRECTLY ANSWERED Q"].sum()
# total_questions = len(df)

# 3. from statistic depend how questions will be given

# 4. do not show questions that are disabled


    # import pandas as pd
    # df = pd.read_csv('statistics.csv', usecols=['QUESTION'])

    # summary = df.describe()

    # question_counts = df.groupby('QUESTION').size().reset_index(name='counts')

    # print(question_counts)