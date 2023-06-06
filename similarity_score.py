import csv
import datetime
import spacy
from tqdm import tqdm

start_time = datetime.datetime.now()

nlp = spacy.load("en_core_web_lg")

categories = ['ADDRESS', 'CARDINAL', 'DECIMAL', 'ELECTRONIC', 'DATE', 'DIGIT', 'FRACTION', 'LETTERS', 'MEASURE',
              'MONEY', 'ORDINAL', 'TELEPHONE', 'TIME', 'VERBATIM']

for category in tqdm(categories):
    lines = 0
    total_similarity = 0

    with open('rs_align_96.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Skip the header 
        next(reader)
        for row in reader:
            # Check if the first column is the current category
            if row[0] == category and row[2] and row[3]:
                # Parse the text in the 3rd and 4th columns
                doc1 = nlp(row[2])
                doc2 = nlp(row[3])
                similarity = doc1.similarity(doc2)
                if similarity > 0:
                    total_similarity += similarity
                    lines += 1
                    
        if lines > 0:
            mean_similarity = total_similarity / lines
            print(f"Total similarity score for {category}: {total_similarity}")
            print(f"The occurrence of {category}: {lines}")
            print(f"Mean similarity score for {category}: {mean_similarity}\n\n")

end_time = datetime.datetime.now()
print(end_time - start_time)
