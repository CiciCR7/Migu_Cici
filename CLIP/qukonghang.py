def remove_empty_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 去除空行
    non_empty_lines = [line for line in lines if line.strip()]

    # 写入新文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(non_empty_lines)

# 使用函数
input_filename = r'D:\vscode-project\prompt\prompt_9_19.txt'  # 需要处理的文件名
output_filename = r'D:\vscode-project\prompt\prompt_9_19.txt'   # 结果输出的文件名

remove_empty_lines(input_filename, output_filename)