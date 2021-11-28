import time
import csv
import os

def dump_to_csv(filename: str, data_list: list):
    full_filename = f"filtered_data/{filename}_{time.strftime('%H%M%S')}.csv"
    with open(full_filename, "w") as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for line in data_list:
            writer.writerow(line)
    return full_filename

def quick_plot(filename):
    pass