import csv


def write_to_file(filepath, row):
    with open(filepath, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(row)
