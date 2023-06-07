import pandas as pd
from tabulate import tabulate

class CSVPrinter:
    def __init__(self, filename):
        self.filename = filename

    def print_csv_info(self):
        data = pd.read_csv(self.filename)
        print(tabulate(data, headers='keys', tablefmt='simple'))

# Usage
def statistics_mode():
    csv_printer = CSVPrinter('statistics.csv')
    csv_printer.print_csv_info()
