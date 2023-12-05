import csv
import datetime

from myfinances.importers.import_statement import ImportStatement


def import_transactions(csv_path):
    lines = []
    with open(csv_path, encoding='latin-1') as csv_file:
        for line in csv.reader(csv_file, delimiter=';'):
            if len(line) < 5:
                continue
            try:
                lines.append(ImportStatement(
                    book_date=datetime.datetime.strptime(line[1], '%d.%m.%Y').date(),
                    transaction_date=datetime.datetime.strptime(line[0], '%d.%m.%Y').date(),
                    account=line[3],
                    notes=line[4],
                    iban=line[5],
                    amount=float(line[7].replace('.', '').replace(',', '.'))
                    ))
            except ValueError:
                # first line contains headers
                pass
    return lines
