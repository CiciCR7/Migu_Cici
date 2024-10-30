import os

def count_images_in_folder(folder_path):
    # 定义支持的图片扩展名
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

    # 初始化计数器
    image_count = 0

    # 遍历文件夹
    for filename in os.listdir(folder_path):
        # 检查文件是否是图片
        if os.path.isfile(os.path.join(folder_path, filename)):
            if os.path.splitext(filename)[1].lower() in image_extensions:
                image_count += 1

    return image_count

# 示例用法
folder_path = '/appsharedata/duzongcai/20240923-photos-wqq/Retrieval_Image_Data_0923ready/all_notchinese-0923'  # 替换为你的文件夹路径
image_count = count_images_in_folder(folder_path)
print(f"文件夹中图片的数量: {image_count}")
