import os
import tarfile
import argparse

def extract_tar_files(input_folder, output_folder):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 检查文件是否以 '.tar' 结尾，并且在 '.tar' 之前的尾部是 'ready'
        if filename.endswith('.tar') and filename[:-4].endswith('ready'):
            file_path = os.path.join(input_folder, filename)
            print(f"正在解压文件: {file_path}")
            try:
                # 打开并解压 tar 文件
                with tarfile.open(file_path, 'r') as tar_ref:
                    tar_ref.extractall(output_folder)
                print(f"成功解压至: {output_folder}")
            except Exception as e:
                print(f"解压文件 {filename} 时出错: {e}")

def main():
    parser = argparse.ArgumentParser(description="解压所有符合条件的 tar 文件")
    parser.add_argument('input_folder', type=str, help='包含 tar 文件的输入文件夹')
    parser.add_argument('output_folder', type=str, help='解压目标文件夹')

    args = parser.parse_args()

    extract_tar_files(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
    
