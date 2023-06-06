import pandas as pd
import csv
import regex as re
import string
import datetime
from tqdm import tqdm

start_time = datetime.datetime.now()

with open('output_6_sent_rSpeak_copy.txt', 'r', encoding = "ISO-8859-1") as f:
    sentences = [line.strip() for line in f]

with open('with_sent_6.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # header
    writer.writerow(['Semiotic Class', 'Input Token', 'Output Token', 'RS'])
    
    with open('output_96.csv', 'r') as csvfile_in:
        reader = csv.reader(csvfile_in)
        next(reader)  # Skip header row.
        current_sentence = ""
        row = next(reader, None)
        for row in reader:
            # If the first column is <eos>, get the next sentence.
            if row[0] == "<eos>":
                try:
                    current_sentence = sentences.pop(0)
                except IndexError:
                    pass

            # Write the row with the current sentence.
            writer.writerow([row[0], row[1], row[2], current_sentence])


df = pd.read_csv("with_sent_6.csv", header=0)

# store the values of VT Output
col5 = []
'''col1:semiotic class
   col2:input token
   col3:output token
   col4:the sentence of VT output
   col5:the normalized word or phrase of VT output.'''


def add_full_stop(sentence):
    if not sentence.endswith(string.punctuation):
        sentence += "."
    return sentence


def get_occur(prev_str, curr_str, next_str):
    start_occur = []
    end_occur = []

    start_regex = r"[\s\p{P}]*\b" + re.escape(str(prev_str)) + r"[\s\p{P}]*\b"

    # r"[\s\p{P}]*\b" cannot match full stop '.' but can match the word boundary
    if next_str == '.':
        end_regex = r"[\s\p{P}]*" + re.escape(str(next_str)) + r"[\s\p{P}]*"
        # print(end_regex)
    else:
        end_regex = r"[\s\p{P}]*\b" + re.escape(str(next_str)) + r"[\s\p{P}]*\b"

    start_matches = re.finditer(start_regex, curr_str)
    end_matches = re.finditer(end_regex, curr_str)

    for match in start_matches:
        if prev_str is not None:
            start_occur.append(match.start() + len(prev_str))
    for match in end_matches:
        if match is not None:
            end_occur.append(match.start())
    return start_occur, end_occur


def get_occur1(curr_str, next_str):
    start_occur = [0]
    end_occur = []

    if next_str == '.':
        end_regex = r"[\s\p{P}]*" + re.escape(str(next_str)) + r"[\s\p{P}]*"
    else:
        end_regex = r"[\s\p{P}]*\b" + re.escape(str(next_str)) + r"[\s\p{P}]*\b"

    end_matches = re.finditer(end_regex, curr_str)

    for match in end_matches:
        if match is not None:
            end_occur.append(match.start())
    return start_occur, end_occur


def get_occur2(prev_str, curr_str):
    start_occur = []
    end_occur = [0]

    start_regex = r"[\s\p{P}]*\b" + re.escape(str(prev_str)) + r"[\s\p{P}]*\b"
    end_matches = re.finditer(start_regex, curr_str)

    for match in end_matches:
        if match is not None:
            end_occur.append(match.start())
    return start_occur, end_occur


def find_min_diff(curr_str):
    start_occur, end_occur = get_occur(prev_str, curr_str, next_str)
    min_diff = len(curr_str)
    start_index = 0
    end_index = 0
    for start in start_occur:
        for end in end_occur:
            if start > end:
                continue
            diff = end - start
            if diff < min_diff:
                min_diff = diff
                start_index = start
                end_index = end
    content = curr_str[start_index + 1:end_index]
    content = re.sub(r'^[%s]+' % string.punctuation, '', content)
    content = re.sub(r'[%s]+$' % string.punctuation, '', content)
    return content.strip()  # delete space


def find_min_diff1(curr_str):
    start_occur, end_occur = get_occur1(curr_str, next_str)
    min_diff = len(curr_str)
    start_index = 0
    end_index = 0
    for end in end_occur:
        diff = end
        if diff < min_diff:
            min_diff = diff
            end_index = end
    content = curr_str[start_index:end_index]
    content = re.sub(r'^[%s]+' % string.punctuation, '', content)
    content = re.sub(r'[%s]+$' % string.punctuation, '', content)
    return content.strip()  # delete space


def find_min_diff2(curr_str):
    start_occur, end_occur = get_occur2(prev_str, curr_str)
    min_diff = len(curr_str)
    start_index = 0
    end_index = 0
    for start in start_occur:
        diff = start
        if diff < min_diff:
            min_diff = diff
            start_index = start
    content = curr_str[start_index:end_index]
    content = re.sub(r'^[%s]+' % string.punctuation, '', content)
    content = re.sub(r'[%s]+$' % string.punctuation, '', content)
    return content.strip()  # delete space


# the loop starts at 2 and iterates up to 5 to make sure to find next_str in next 5 words
def end_is_none(next_str):
    for j in range(2, 6):
        if i + j < len(df) and str(df.iloc[i + j][1]) != '<eos>':
            next_str = str(df.iloc[i + j][1])
            break
        else:
            next_str = None
    return next_str


def start_is_none(prev_str):
    for j in range(2, 6):
        if i + j < len(df) and str(df.iloc[i - j][1]) != '<eos>':
            prev_str = str(df.iloc[i - j][1])
            break
        else:
            prev_str = None
    return prev_str


df.loc[df['Input Token'] == 'vol', 'Input Token'] = 'Volume'
df.loc[df['Input Token'] == '-', 'Input Token'] = 'to'  # '-' is normalized as 'to' but masrked as 'PLAIN'
df['RS'] = df['RS'].astype(str).apply(add_full_stop)  # add full stop to 'VT' column

for i, row in tqdm(df.iterrows(), total=df.shape[0]):
#for i, row in df.iterrows():
    # sentence = row['VT']  # !!!!Rs
    # new_sentence = add_full_stop(str(sentence))
    # row['VT'] = new_sentence
    # df.loc[df['Input Token'] == 'vol', 'Input Token'] = 'Volume'
    # df.loc[df['Input Token'] == '-', 'Input Token'] = 'to'  # '-' is normalized as 'to' but masrked as 'PLAIN'
    if row["Semiotic Class"] in ["PUNCT", "PLAIN"]:
        col5.append(str(row["Input Token"]).lower())
    elif row["Semiotic Class"] == "<eos>":
        col5.append("")  # skip the row
    else:
        prev_plain = df.iloc[i - 1]["Semiotic Class"] == "PLAIN" if i > 0 else False
        next_plain = df.iloc[i + 1]["Semiotic Class"] == "PLAIN" if i < len(df) - 1 else False
        prev_eos = df.iloc[i - 1]["Semiotic Class"] == "<eos>" if i > 0 else False
        next_eos = df.iloc[i + 1]["Semiotic Class"] == "<eos>" if i < len(df) - 1 else False
        # check if the previous row is "PLAIN" and the next row is "PUNCT"
        prev_punct = df.iloc[i - 1]["Semiotic Class"] == "PUNCT" if i > 0 else False
        next_punct = df.iloc[i + 1]["Semiotic Class"] == "PUNCT" if i < len(df) - 1 else False

        # check if the previous and next rows both are "PLAIN" or 'PUNCT'
        # check if the previous row is "PUNCT" and the next row is "PLAIN"
        # check if the previous row is "PLAIN" and the next row is "PUNCT"
        if (prev_plain and next_plain) or (prev_punct and next_punct) or (prev_punct and next_plain) or (
                prev_plain and next_punct):
            prev_str = str(df.iloc[i - 1][1])
            curr_str = str(df.iloc[i][3])
            next_str = str(df.iloc[i + 1][1])


            start_occur, end_occur = get_occur(prev_str, curr_str, next_str)


            # content = find_min_diff(curr_str)

            if start_occur and end_occur:
                # content = find_min_diff(curr_str)
                pass
            else:
                if not start_occur and end_occur:
                    prev_str = start_is_none(prev_str)
                elif not end_occur and start_occur:
                    next_str = end_is_none(next_str)
                else:
                    if i - 2 > 0 and i + 2 < len(df) and str(df.iloc[i - 2][1]) != '<eos>' and str(
                            df.iloc[i + 2][1]) != '<eos>':
                        prev_str = str(df.iloc[i - 2][1])
                        next_str = str(df.iloc[i + 2][1])

                        if i - 3 > 0 and i + 3 < len(df) and str(df.iloc[i - 2][1]) != '<eos>' and str(
                                df.iloc[i + 2][1]) != '<eos>':
                            prev_str = str(df.iloc[i - 3][1])
                            next_str = str(df.iloc[i + 3][1])
                        else:
                            next_str = None
                    else:
                        prev_str = None
                        next_str = None
            content = find_min_diff(curr_str)

            # col5.append(content)

        # check if the previous row is "<eos>" and the next row is "PLAIN"
        # check if the previous row is "<eos>" and the next row is "PUNCT"
        elif (prev_eos and next_plain) or (prev_eos and next_punct):
            curr_str = str(df.iloc[i][3])
            next_str = str(df.iloc[i + 1][1])
            start_occur, end_occur = get_occur1(curr_str, next_str)
            if not end_occur and start_occur:
                next_str = end_is_none(next_str)
            content = find_min_diff1(curr_str)

        # check if the previous row is "PLAIN" and the next row is "<eos>"
        # check if the previous row is "PUNCT" and the next row is "<eos>"
        elif (prev_plain and next_eos) or (prev_punct and next_eos):
            prev_str = str(df.iloc[i - 1][1])
            curr_str = str(df.iloc[i][3])
            start_occur, end_occur = get_occur2(prev_str, curr_str)
            if not start_occur and end_occur:
                prev_str = start_is_none(prev_str)
            content = find_min_diff2(curr_str)
        else:
            # col5.append("")  # skip the row
            content = ' '
        col5.append(content.lower())


df["RS Output"] = col5
df = df.drop(['RS'], axis=1)  # !!!!RS

mask = (df["Semiotic Class"] == "CARDINAL") & (df["RS Output"].str.startswith('e'))
df.loc[mask, "RS Output"] = df.loc[mask, "RS Output"].str[2:]

df.to_csv("rs_align_6.csv", index=False)

end_time = datetime.datetime.now()
print(end_time - start_time)
