import csv


def get_transactions_from_csv(csv_file: str) -> list[dict]:
    transactions = []
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

    return transactions
