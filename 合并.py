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

    # 重命名后面的列名为"文件名+列名"
    new_columns = df.columns[:3].tolist() + [f"{file_name}_{col}" for col in df.columns[3:]]
    df.columns = new_columns

    # 保留前三列并去重
    if merged_df is None:
        merged_df = df
    else:
        # 合并数据，按前三列作为key，保留一次相同的前三列
        merged_df = pd.merge(merged_df, df, on=new_columns[:3], how='outer')

# 删除完全重复的前三列数据
merged_df.drop_duplicates(subset=merged_df.columns[:3], inplace=True)

# 将合并后的数据写入新的csv文件
merged_df.to_csv(output_file, sep=csv_separator, index=False)

print(f'合并后的CSV文件已保存为: {output_file}')
