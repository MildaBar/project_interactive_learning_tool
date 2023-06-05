from questions import count_questions
# SELECT THE NR OF QUESTIONS FOR THE TEST WHICH IS NOT LARGER THAN THE TOTAL NUMBER OF QUESTIONS ADDED
def test():
    print("You chose to have a test! Let's start!")
    check_question()
    
def check_question():
    while True:
        try:
            question_num = int(input("Select number of questions for the test: "))
            if question_num > count_questions("statistics.csv"):
                print("Selected number of questions are larger than the total number of questions adeded. Try again.")
            else:
                break
        except ValueError:
            print("You didn't chooce any number of questions. Try again.")


test()

# THE QUESTIONS ARE CHOSEN FULLY RANDOMLY AND DEPEND OF DISABLE/ENABLE

# EACH QUESTION CAN ONLY APPEAR ONCE AT THE MOST IN THE TEST

# AT THE END OF THE QUESTIONS, THE USER IS SHOWS SCORE

# THE LIST OF SCORES SHOULD BE SAVED IN A SEPERATE results.txt FILE - THE DATE AND TIME SHOULD BE ADDED NEXT TO THE SCORE AS WELL