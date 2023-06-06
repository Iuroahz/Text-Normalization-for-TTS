import csv
import datetime
import spacy
from tqdm import tqdm

start_time = datetime.datetime.now()
nlp = spacy.load("en_core_web_lg")

# categories = ['ADDRESS', 'CARDINAL', 'DECIMAL', 'ELECTRONIC', 'DATE', 'DIGIT', 'FRACTION', 'LETTERS', 'MEASURE',
# 'MONEY', 'ORDINAL', 'TELEPHONE', 'TIME', 'VERBATIM']


categories = ['ADDRESS', 'CARDINAL', 'DECIMAL', 'ELECTRONIC', 'DATE', 'DIGIT', 'FRACTION', 'LETTERS', 'MEASURE',
              'MONEY', 'ORDINAL', 'TELEPHONE', 'TIME', 'VERBATIM']


for category in tqdm(categories):
    #total_similarity = 0
    lines = 0
    with open("vt_align_1.csv", "r") as vt_input, open(f"vt_{category}.csv", "w", newline="") as output_file:
        reader_vt = csv.reader(vt_input)
        #reader_rs = csv.reader(rs_input)
        writer = csv.writer(output_file)

        # header
        writer.writerow(["Semiotic Class", "Input Token", "Output Token", "VT Output", "Similarity"])

        for row in reader_vt:
            if row[0] == category and row[2] and row[3]:
                # Parse the text in "Output Token",	"VT Output"
                doc1 = nlp(row[2])
                doc2 = nlp(row[3])
                similarity = doc1.similarity(doc2)
                #if similarity > 0:
                    #total_similarity += similarity
                    #lines += 1
                lines += 1
                writer.writerow([row[0], row[1], row[2], row[3], similarity])
                if lines > 200:
                    break

for category in tqdm(categories):
    # total_similarity = 0
    lines = 0
    with open("rs_align_1.csv", "r") as rs_input, open(f"rs_{category}.csv", "w", newline="") as output_file:
        reader_rs = csv.reader(rs_input)
        writer = csv.writer(output_file)

        # header
        writer.writerow(["Semiotic Class", "Input Token", "Output Token", "VT Output", "Similarity"])

        for row in reader_rs:
            if row[0] == category and row[2] and row[3]:
                # Parse the text in "Output Token",	"RS Output"
                doc1 = nlp(row[2])
                doc2 = nlp(row[3])
                similarity = doc1.similarity(doc2)
                lines += 1
                writer.writerow([row[0], row[1], row[2], row[3], similarity])
                if lines > 200:
                    break


end_time = datetime.datetime.now()
print(end_time - start_time)
