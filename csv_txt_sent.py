import csv
import datetime
import pandas as pd
from tqdm import tqdm

start_time = datetime.datetime.now()

df = pd.read_csv("output_1000.csv", header=0)
with open('sentences.txt', 'w') as txt_file:
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        prev_row = df.iloc[i - 1]["Semiotic Class"]
        if row["Semiotic Class"] == ["PLAIN"]:
            if prev_row == ["PLAIN"]:
                txt_file.write(' '+ df.iloc[i]["Input Token"])
            elif prev_row == ["PUNCT"] or prev_row is None:
                txt_file.write(row[1])
        elif row["Semiotic Class"] == ["PUNCT"]:
            if prev_row == ["PLAIN"] or prev_row is None:
                txt_file.write(row[1])
            elif prev_row == ["PUNCT"]:
                txt_file.write(row[1])
        elif row["Semiotic Class"] == ["<eos>"]:
                txt_file.write('\n')
        else:
            txt_file.write(' ' + str(row[2]))


'''with open('output_1000.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    df = pd.read_csv("output_1000.csv", header=0)
    with open('sentences.txt', 'w') as txt_file:
        prev_row = df.iloc[i - 1]["Semiotic Class"] == "PUNCT"
        for row in csv_reader:
            if row[0] == 'PLAIN':
                txt_file.write(row[1] + ' ')
                prev_row = row
            elif row[0] == 'PUNCT':
                if prev_row and prev_row[0] == 'PLAIN':
                    txt_file.write(row[1])
                else:
                    txt_file.write(row[1] + ' ')
                prev_row = row
            elif row[0] == '<eos>':
                txt_file.write('\n')
                prev_row = None
            else:
                txt_file.write(' ' + row[2])
                prev_row = row'''

end_time = datetime.datetime.now()
print(end_time - start_time)