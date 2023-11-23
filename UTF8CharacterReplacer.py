filename = "/Users/zonghang/Desktop/yingying/test.csv"  # 替换为您的文件名

def replace_invalid_utf8_characters(filename):
    try:
        # 尝试以 UTF-8 格式打开并读取文件内容
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # 如果遇到编码错误，则处理这些错误
        with open(filename, 'rb') as file:
            content_bytes = file.read()

        # 找到所有无法解码的字符
        invalid_chars = set()
        start = 0
        while start < len(content_bytes):
            try:
                content_bytes[start:start+1].decode('utf-8')
                start += 1
            except UnicodeDecodeError:
                invalid_chars.add(content_bytes[start:start+1])
                start += 1

        # 对每个无效字符进行替换
        replacements = {}
        for char in invalid_chars:
            print(f"无法识别的字符: {char}")
            replacement = input("请输入替换字符: ")
            replacements[char] = replacement

        # 替换所有无效字符
        new_content = ""
        start = 0
        while start < len(content_bytes):
            if content_bytes[start:start+1] in replacements:
                new_content += replacements[content_bytes[start:start+1]]
                start += 1
            else:
                try:
                    new_content += content_bytes[start:start+1].decode('utf-8')
                    start += 1
                except UnicodeDecodeError:
                    # 正常情况下不应该到达这里
                    start += 1

        # 保存更改
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(new_content)

        print("文件已更新为 UTF-8 编码。")
    else:
        print("文件已成功以 UTF-8 格式读取，无需更改。")


replace_invalid_utf8_characters(filename)
