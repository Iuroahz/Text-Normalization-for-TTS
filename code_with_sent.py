import csv
import pandas as pd

df = pd.read_csv("/proj/uppmax2020-2-2/zhaorui/with_vt_sentence.csv")

# output tokens list
col5 = []

'''col1:semiotic class
   col2:input token
   col3:output token
   col4:the sentence of RS output
   col5:the normalized word or phrase of RS output.''' 
for i, row in df.iterrows():
    if row["Semiotic Class"] in ["PUNCT", "PLAIN"]:
        col5.append(row["Input Token"])
    elif row["Semiotic Class"] == "<eos>":
        col5.append("")  # skip the row
    else:
        prev_plain = df.iloc[i-1]["Semiotic Class"] == "PLAIN" if i > 0 else False
        next_plain = df.iloc[i+1]["Semiotic Class"] == "PLAIN" if i < len(df)-1 else False
        prev_eos = df.iloc[i-1]["Semiotic Class"] == "<eos>" if i > 0 else False
        next_eos = df.iloc[i+1]["Semiotic Class"] == "<eos>" if i < len(df)-1 else False
        # check if the previous row is "PLAIN" and the next row is "PUNCT"
        prev_punct = df.iloc[i-1]["Semiotic Class"] == "PUNCT" if i > 0 else False
        next_punct = df.iloc[i+1]["Semiotic Class"] == "PUNCT" if i < len(df)-1 else False
     
         
        # check if the previous and next rows are "PLAIN"
        # check if the previous row is "PUNCT" and the next row is "PLAIN"
        # check if the previous row is "PLAIN" and the next row is "PUNCT"
        if (prev_plain and next_plain) or (prev_punct and next_punct) or (prev_punct and next_plain) or (prev_plain and next_punct):
            prev_str = str(df.iloc[i-1][1])
            #print(prev_str)
            curr_str = str(df.iloc[i][3])
            #print(curr_str)
            next_str = str(df.iloc[i+1][1])
            #print(next_str)
            start_index = curr_str.find(prev_str) + len(prev_str) 
            end_index = curr_str.find(next_str)  
            content = curr_str[start_index:end_index]
            col5.append(content)

        # check if the previous row is "<eos>" and the next row is "PLAIN"
        # check if the previous row is "<eos>" and the next row is "PUNCT"
        elif (prev_eos and next_plain) or (prev_eos and next_punct):
            curr_str = str(df.iloc[i][3])
            next_str = str(df.iloc[i+1][1])
            end_index = curr_str.find(next_str)
            content = curr_str[:end_index]
            col5.append(content)

        # check if the previous row is "PLAIN" and the next row is "<eos>"
        # check if the previous row is "PUNCT" and the next row is "<eos>"
        elif (prev_plain and next_eos) or (prev_punct and next_eos):
            prev_str = str(df.iloc[i-1][1])
            curr_str = str(df.iloc[i][3])
            start_index = curr_str.find(prev_str) + len(prev_str)
            content = curr_str[start_index:]
            col5.append(content)
        else:
            col5.append("")  # skip the row

df["RS Output"] = col5

# Delete sentence
df=df.drop(['RS'],axis=1)

df.to_csv("rs_align_1.csv", index=False)

#! tail -n 100 rs_align_1.csv
