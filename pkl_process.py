import pickle
import warnings
from tqdm import tqdm
from collections import defaultdict

warnings.filterwarnings('ignore')

with open('norm_texts_weights_100_input_91_sent_output_91_sentences_merged.txt_-1_0.2.pkl', 'rb') as f:
    data = pickle.load(f)

def save_to_txt(results, filename):
    with open(filename, 'w') as file:
        for result in results:
            file.write(result + '\n')

def process_data(data):
    result_list = []

    for strings, scores in tqdm(data, desc="Processing data", unit="tuple"):
        max_score_index = scores.index(max(scores))
        result_list.append(strings[max_score_index])

    return result_list

result = process_data(data)
save_to_txt(result, "result_sentence.txt")
