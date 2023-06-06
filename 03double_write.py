import os
from tqdm import tqdm

folder1 = "/data1/xczhou/project/test_code2/NeMo-text-processing/data/sentences"  # 替换为你的第一个文件夹路径
folder2 = "/data1/xczhou/project/test_code2/NeMo-text-processing/data/sentences_new"  # 替换为你的第二个文件夹路径
output_folder = "/data1/xczhou/project/test_code2/NeMo-text-processing/data/sentences_merge"  # 替换为你的输出文件夹路径

max_rows = float('inf')  # 设置要处理的最大行数
max_rows = 8000  # 设置要处理的最大行数

# 如果输出文件夹不存在，则创建它
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 获取并排序两个文件夹中的 txt 文件
txt_files1 = sorted([file for file in os.listdir(folder1) if file.endswith(".txt")])
txt_files2 = sorted([file for file in os.listdir(folder2) if file.endswith(".txt")])

# 对应地将两个文件夹中的文件逐行交替写入到新的 txt 文件中
for file1, file2 in tqdm(zip(txt_files1, txt_files2), total=len(txt_files1), desc="合并文件"):
    with open(os.path.join(folder1, file1), "r") as f1, open(os.path.join(folder2, file2), "r") as f2:
        # 检查两个文件的行数是否相同
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        if len(lines1) != len(lines2):
            print(f"警告：文件 {file1} 和 {file2} 的行数不同！")

        # 创建新的文件名
        output_filename = f"{os.path.splitext(file1)[0]}_{os.path.splitext(file2)[0]}_merged.txt"
        output_path = os.path.join(output_folder, output_filename)

        # 将两个文件逐行交替写入到新的 txt 文件中
        with open(output_path, "w") as output_file:
            for i, (line1, line2) in enumerate(zip(lines1, lines2)):
                if i >= max_rows:
                    break
                output_file.write(line1.rstrip() + "~~RAW\n")  # 在第一个文件的每一行后面加上~~RAW
                output_file.write(line2.rstrip() + "~~1\n")  # 在另一个文件的每一行后面加上~~1
                output_file.write("\n")  # 每次交替写入后空一行

print("处理完成！")