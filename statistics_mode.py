import pandas as pd

pd.set_option(
    "display.max_colwidth", 25
)  # set the maximum column width for displaying data frames in pandas to 100 characters


def statistics_mode():
    file = "statistics.csv"
    open_file = open(file, "r")
    read_file = pd.read_csv(file)
    print(read_file)
