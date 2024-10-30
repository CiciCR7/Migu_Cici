import os
import shutil

def process_folders(input_folder, all_chinese_folder, all_notchinese_folder):
    # 创建目标文件夹
    os.makedirs(all_chinese_folder, exist_ok=True)
    os.makedirs(all_notchinese_folder, exist_ok=True)

    # 计数变量
    total_chinese_moved = 0
    total_notchinese_moved = 0

    # 遍历输入文件夹
    for root, dirs, files in os.walk(input_folder):
        for dir_name in dirs:
            # 构建中文件夹和非中文件夹的路径
            chinese_folder = os.path.join(root, dir_name, 'chinese')
            not_chinese_folder = os.path.join(root, dir_name, 'not_chinese')

            # 如果存在chinese文件夹，移动其中的文件
            if os.path.exists(chinese_folder):
                for file_name in os.listdir(chinese_folder):
                    src_file = os.path.join(chinese_folder, file_name)
                    if os.path.isfile(src_file):
                        shutil.move(src_file, all_chinese_folder)
                        total_chinese_moved += 1  # 增加计数
                        print(f"移动: {src_file} 到 {all_chinese_folder}")

            # 如果存在not_chinese文件夹，移动其中的文件
            if os.path.exists(not_chinese_folder):
                for file_name in os.listdir(not_chinese_folder):
                    src_file = os.path.join(not_chinese_folder, file_name)
                    if os.path.isfile(src_file):
                        shutil.move(src_file, all_notchinese_folder)
                        total_notchinese_moved += 1  # 增加计数
                        print(f"移动: {src_file} 到 {all_notchinese_folder}")

    # 输出移动的文件数量
    print(f"\n总共移动了 {total_chinese_moved} 个Chinese和 {total_notchinese_moved} 个not_chiense。")

def main():
    input_folder = '/sharedata/duzongcai/data/Retrieval_Image_Data_0923ready'  # 替换为你的大文件夹路径
    all_chinese_folder = 'sharedata/duzongcai/data/Retrieval_Image_Data_0923ready/all_chinese-0923'  # 替换为你的目标中文件夹路径
    all_notchinese_folder = 'sharedata/duzongcai/data/Retrieval_Image_Data_0923ready/all_notchinese-0923'  # 替换为你的目标非中文件夹路径

    process_folders(input_folder, all_chinese_folder, all_notchinese_folder)

if __name__ == "__main__":
    main()
