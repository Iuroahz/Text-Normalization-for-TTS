import os
import re
from tqdm import tqdm

output_folder = '/data1/xczhou/project/test_code2/NeMo-text-processing/data/sentence_result'  # 替换为你的输出文件夹路径
processed_folder = '/data1/xczhou/project/test_code2/NeMo-text-processing/data/sentences_new'  # 替换为处理后文件的输出文件夹路径

# 如果处理后的文件夹不存在，则创建它
if not os.path.exists(processed_folder):
    os.makedirs(processed_folder)

txt_files = [file for file in os.listdir(output_folder) if file.endswith('.txt')]

print(f"开始处理 {len(txt_files)} 个 TXT 文件...")

for file in tqdm(txt_files):
    input_path = os.path.join(output_folder, file)
    output_path = os.path.join(processed_folder, file)

    with open(input_path, 'r') as input_file:
        content = input_file.read()

    # 替换双引号或括号后的多余空格
    content = re.sub(r'\" ', '"', content)
    content = re.sub(r'\( ', '(', content)

    with open(output_path, 'w') as output_file:
        output_file.write(content)

print("处理完成！")
