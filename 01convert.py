import os
import csv
from tqdm import tqdm

input_folder = '/data1/xczhou/project/test_code2/NeMo-text-processing/data/sentence/'  # 替换为你的 CSV 文件夹路径
output_folder = '/data1/xczhou/project/test_code2/NeMo-text-processing/data/sentence_result/'  # 替换为你的输出文件夹路径
max_rows = float('inf')  # 设置要处理的最大行数

# 如果输出文件夹不存在，则创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

print(f"开始处理 {len(csv_files)} 个 CSV 文件...")

for file in csv_files:
    input_path = os.path.join(input_folder, file)
    output_filename = os.path.splitext(file)[0] + '_sentences.txt'
    output_path = os.path.join(output_folder, output_filename)

    with open(input_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        # 获取文件行数，以便设置进度条
        total_rows = min(sum(1 for row in csv_file) - 1, max_rows)
        csv_file.seek(0)  # 将文件指针返回到文件开头
        next(csv_reader)  # 跳过标题行

        with open(output_path, 'w') as txt_file:
            prev_char = None
            for row in tqdm(csv_reader, total=total_rows, desc=f"处理 {file}"):
                content = row[1] if row[0] == 'PLAIN' else row[2]

                if prev_char and content not in {'"', '(', "“", "”"} and prev_char not in {' ', '\n'} and row[0] != 'PUNCT':
                    txt_file.write(' ')

                if row[0] == 'PLAIN':
                    txt_file.write(row[1])
                    prev_char = row[1][-1]
                elif row[0] == 'PUNCT':
                    if row[1] not in {',', '.', '!', '?', ';', ':', "''", "\"", "“", "”", "(", ")", "[", "]", "{", "}"}:
                        txt_file.write(' ')
                    txt_file.write(row[1])
                    prev_char = row[1][-1]
                elif row[0] == '<eos>':
                    txt_file.write('\n')
                    prev_char = '\n'
                else:
                    txt_file.write(row[2])
                    prev_char = row[2][-1]

                # 修复双引号和括号后的空格问题
                if content in {'"', '(', "“", "”"}:
                    continue

                total_rows -= 1
                if total_rows <= 0:
                    break

print("处理完成！")