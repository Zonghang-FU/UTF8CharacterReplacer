import os
import pandas as pd

# 定义输入和输出文件夹路径
input_folder = 'your/input/folder/path'  # 文件路径
output_file = input_folder+ '/output.csv' 
csv_separator = ','  




# 获取文件夹下所有的csv文件
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# 初始化一个空的dataframe用于存储合并后的数据
merged_df = None

for csv_file in csv_files:
    # 读取每个csv文件，跳过空白列
    csv_path = os.path.join(input_folder, csv_file)
    df = pd.read_csv(csv_path, sep=csv_separator)

    # 删除全空的列
    df.dropna(axis=1, how='all', inplace=True)

    # 获取文件名并移除扩展名
    file_name = os.path.splitext(csv_file)[0]

    # 只保留第二列作为key以及后面的列
    df_key = df.iloc[:, [2]].copy()  # 第三列作为key
    df_rest = df.iloc[:, 3:].copy()  # 忽略前三列，保留后面的列

    # 修改后面列的列名为 "文件名+列名"
    new_columns = [f"{file_name}_{col}" for col in df_rest.columns]
    df_rest.columns = new_columns

    # 合并key和数据部分
    df_final = pd.concat([df_key, df_rest], axis=1)

    # 如果merged_df为空，则直接赋值第一个文件的内容
    if merged_df is None:
        merged_df = df_final
    else:
        # 按第三列的key进行外连接合并
        merged_df = pd.merge(merged_df, df_final, on=df_key.columns[0], how='outer')

# 将合并后的数据写入新的csv文件，不包括前三列的内容
merged_df.to_csv(output_file, sep=csv_separator, index=False)

print(f'合并后的CSV文件已保存为: {output_file}')
