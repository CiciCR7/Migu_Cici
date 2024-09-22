import torch
import clip
from PIL import Image
import os
import numpy as np
import shutil
import torch.nn.functional as F
from tqdm import tqdm



#参数配置
# 分批提取图片特征
batch_size = 64
# 设定相似度阈值
similarity_threshold = 0.85


# 定义图片文件夹路径
image_folder = r'D:\vscode-project\chinese_migu_0'
output_base_folder = r'D:\vscode-project\chinese_wangqiqi'
os.makedirs(output_base_folder, exist_ok=True)

# 加载 CLIP 模型
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# 定义图片文件夹路径
image_folder = r'D:\vscode-project\chinese_migu'
output_base_folder = r'D:\vscode-project\chinese_wangqiqi'
os.makedirs(output_base_folder, exist_ok=True)

# 加载所有图片路径
image_paths = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('png', 'jpg', 'jpeg'))]
image_names = [os.path.basename(path) for path in image_paths]

# 分批提取图片特征
image_features_list = []
for i in tqdm(range(0, len(image_paths), batch_size), desc="Processing batches"):
    batch_images = image_paths[i:i+batch_size]
    batch_tensors = [preprocess(Image.open(img)).unsqueeze(0).to(device) for img in batch_images]
    batch_tensors = torch.cat(batch_tensors, dim=0)

    with torch.no_grad():
        batch_features = model.encode_image(batch_tensors)
        image_features_list.append(batch_features.cpu())

# 将特征向量拼接成 Tensor
image_features_tensor = torch.cat(image_features_list, dim=0)

# 对特征向量进行归一化
image_features_tensor = F.normalize(image_features_tensor, p=2, dim=1)

# 计算归一化后的特征向量之间的余弦相似度
similarity_matrix = torch.mm(image_features_tensor, image_features_tensor.t()).numpy()


# 生成文件夹和分类图片
visited = set()  # 跟踪已处理的图片
image_to_folder = {}  # 记录图片到文件夹的映射
folder_index = 1

for i in range(len(image_names)):
    if i in visited:
        continue
    
    # 找到与当前图片相似的所有图片
    similar_images = [i]
    for j in range(i + 1, len(image_names)):
        if similarity_matrix[i, j] > similarity_threshold and j not in visited:
            visited.add(j)
            similar_images.append(j)
            
    
    # 创建文件夹并复制图片
    cluster_folder = os.path.join(output_base_folder, f'cluster_{folder_index}_{len(similar_images)}')
    os.makedirs(cluster_folder, exist_ok=True)
    
    for idx in similar_images:
        if idx not in image_to_folder:  # 只复制尚未处理的图片
            shutil.copy(image_paths[idx], cluster_folder)
            image_to_folder[idx] = cluster_folder
    
    folder_index += 1

print("Finished categorizing and copying images.")