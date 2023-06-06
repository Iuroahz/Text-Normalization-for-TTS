from tqdm import tqdm


# 打开原始文件和输出文件
with open('/data1/xczhou/project/test_code2/NeMo-text-processing/data/words/eval_data.txt', 'r') as f_in, \
    open('/data1/xczhou/project/test_code2/NeMo-text-processing/data/words/eval_data_1.txt', 'w') as f_out:
    # 循环读取前3万行
    for i, line in tqdm(enumerate(f_in)):
        if i < 100000:
            f_out.write(line)
        else:
            break
