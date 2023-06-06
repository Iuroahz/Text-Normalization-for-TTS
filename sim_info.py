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
    total_similarity = 0
    lines = 0
    with open("vt_align_1.csv", "r") as vt_input, \
            open("rs_align_1.csv", "r") as rs_input, \
            open(f"{category}.csv", "w", newline="") as output_file:
        reader_vt = csv.reader(vt_input)
        reader_rs = csv.reader(rs_input)
        writer = csv.writer(output_file)

        # header
        writer.writerow(
            ["Semiotic Class", "Input Token", "Output Token", "VT Output", "Similarity", "RS Output", "Similarity"])

        for row_vt in reader_vt:
            if row_vt[0] == category and row_vt[2] and row_vt[3]:
                # Parse the text in "Output Token", "VT Output"
                doc1 = nlp(row_vt[2])
                doc2 = nlp(row_vt[3])
                similarity_vt = doc1.similarity(doc2)
                if similarity_vt > 0:
                    total_similarity += similarity_vt
                    lines += 1
                    row_rs = next(reader_rs)
                    while row_rs[0] != category or not (row_rs[2] and row_rs[3]):
                        row_rs = next(reader_rs)
                    # Parse the text in "Output Token", "RS Output"
                    doc1 = nlp(row_rs[2])
                    doc2 = nlp(row_rs[3])
                    similarity_rs = doc1.similarity(doc2)
                    if similarity_rs > 0:
                        total_similarity += similarity_rs
                        writer.writerow(
                            [row_vt[0], row_vt[1], row_vt[2], row_vt[3], similarity_vt, row_rs[3], similarity_rs])
                        if lines > 1050:
                            break



end_time = datetime.datetime.now()
print(end_time - start_time)
