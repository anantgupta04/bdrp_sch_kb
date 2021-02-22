import csv

file_in = '../data/core_unique.csv'
file_out = '../decoded_data/core_unique.csv'

with open(file_in, encoding='utf-8', errors='ignore') as f:
    reader = csv.reader(f)
    with open(file_out, 'w') as ff:
        writer = csv.writer(ff)
        writer.writerows(reader)