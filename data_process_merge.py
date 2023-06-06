import os
from tqdm import tqdm

folder1 = "/project/test_code2/NeMo-text-processing/data/sentences" 
folder2 = "/project/test_code2/NeMo-text-processing/data/sentences_new" 
output_folder = "/project/test_code2/NeMo-text-processing/data/sentences_merge"

max_rows = float('inf') 
max_rows = 8000 

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

txt_files1 = sorted([file for file in os.listdir(folder1) if file.endswith(".txt")])
txt_files2 = sorted([file for file in os.listdir(folder2) if file.endswith(".txt")])

for file1, file2 in tqdm(zip(txt_files1, txt_files2), total=len(txt_files1), desc="merge"):
    with open(os.path.join(folder1, file1), "r") as f1, open(os.path.join(folder2, file2), "r") as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        if len(lines1) != len(lines2):
            print(f" {file1} and {file2} have different lines")

        output_filename = f"{os.path.splitext(file1)[0]}_{os.path.splitext(file2)[0]}_merged.txt"
        output_path = os.path.join(output_folder, output_filename)

        with open(output_path, "w") as output_file:
            for i, (line1, line2) in enumerate(zip(lines1, lines2)):
                if i >= max_rows:
                    break
                output_file.write(line1.rstrip() + "~~RAW\n")  # add~~RAW
                output_file.write(line2.rstrip() + "~~1\n")  # add~~1
                output_file.write("\n")  # new line after zipping

print("Finished！")
