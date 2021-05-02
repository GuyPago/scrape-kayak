import glob
import pandas as pd
import os


def is_non_empty_file(file):
    return os.path.isfile(file) and os.path.getsize(file) > 0


path = 'Output'
folders = [i for i in glob.glob(path + '//*')]
folder = [i for i in glob.glob(path + '//TLV-KTM' + '//FlightData*.csv')]
print(folders)

combined_csv = []

for j in range(len(folders)):
    for i in glob.glob(folders[j] + '//FlightData*.csv'):
        if is_non_empty_file(i):
            combined_csv.append(pd.read_csv(i, header=None))


# print(pd.concat(combined_csv))
pd.concat(combined_csv).to_csv('FlightData_merged.csv', encoding='utf-8-sig', index=False)
# print(pd.concat(combined_csv, ignore_index=True))
