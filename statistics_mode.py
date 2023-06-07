import pandas as pd

pd.set_option("display.max_colwidth", 100)


def statistics_mode():
    file = "statistics.csv"
    opened = open(file, "r")
    readed = pd.read_csv(file)
    print(readed)
