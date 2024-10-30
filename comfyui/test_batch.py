import json
import os
import random
import requests
import time
import shutil
import pandas as pd

from PIL import Image
#更改自己的url：ip + 端口
URL = "http://192.168.0.2:8188/prompt"

#输出图片路径
INPUT_DIR = "/appsharedata/wangqiqi/comfyui-master/input" 
OUTPUT_DIR = "/appsharedata/wangqiqi/comfyui-master/output/IDM-VTON" 
target_path1 = "/appsharedata/wangqiqi/comfyui-master/image_step1_v1"

ref_image_dir = "/appsharedata/wangqiqi/image_step1_v1"

os.makedirs(OUTPUT_DIR,exist_ok= True)
os.makedirs(target_path1,exist_ok= True)

cached_seed = 0


def get_latest_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image

def get_file_time(file_path):
    return os.path.getmtime(file_path)
    

def start_queue(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data=data)

json_PATH = "/appsharedata/wangqiqi/comfyui-master/workflow_api_huanyi.json"

def generate_image(ref_image_path):
    with open(json_PATH, "r") as file_json:
        prompt = json.load(file_json)
        prompt["11"]["inputs"]["image"] = "1_dress.jpg"
        ref_image = Image.open(ref_image_path)
        if ref_image.mode == 'RGBA':
            mv_image = role_image.convert('RGB')
        seed = random.randint(0,10000000000)
        ref_image.save(os.path.join(INPUT_DIR,"ref_image.jpg"))
        prompt["10"]["inputs"]["image"] = "ref_image.jpg"
        prompt["50"]["inputs"]["seed"] = seed
        # previous_txt_time = get_file_time(txt_file)
        pre_img = get_latest_image(OUTPUT_DIR)
        start_queue(prompt)
        start_time = time.time()
        while True:
            latest_img = get_latest_image(OUTPUT_DIR)
            time.sleep(1)
            end_time = time.time()
            if pre_img != latest_img or end_time - start_time > 90:
                print(end_time-start_time)
                return latest_img

for img_name in os.listdir(ref_image_dir):
    if img_name.endswith(".jpg"):
        ref_image_path = os.path.join(ref_image_dir,img_name)
        res_image_path = generate_image(ref_image_path)
        shutil.copy(res_image_path,os.path.join(target_path1,img_name))
# image_dir = "/appsharedata/hanfubo/mv/output_frames_all"
# txt_file = "/appsharedata/hanfubo/workflows/API/flux_pulid+重绘.json"
# if not os.path.exists(tar_dir):
#         os.makedirs(tar_dir)
# all_dirs = os.listdir(image_dir)
# for dir in all_dirs:
#     if dir.endswith("after"):
#         dir_path = os.path.join(image_dir,dir)
#         for img in os.listdir(dir_path):
#             if img.endswith(".jpg"):
#                 img_file_path = os.path.join(dir_path,img)
#                 generate_image(img_file_path)
        
# filename = "/root/paddlejob/workspace/env_run/output/comfyui_batch/faceswap/flux_test/test_0825.xlsx"
# role_dir = "/root/paddlejob/workspace/env_run/output/comfyui_batch/faceswap/flux_test/role_faces"
# img_path = "/root/paddlejob/workspace/env_run/output/comfyui_batch/faceswap/flux_test/out_flux"
# df = pd.read_excel(filename)
# role_name_list = ["果果","夏婉莹","林雪芙","杨知恩","饶如霜","刘月","姜唐","风尘女人","小丫头","苏祈","吴娇娇","王悍"]
# for index, row in df.iterrows():
#    image_name = int(row["id"])-1
#    role_name = row["人物"]
#    if role_name not in role_name_list:
#        continue
#    if image_name < 24:
#        continue
#    for i in range(3):
#        tar_img_file1 = os.path.join(target_path1, f"{image_name}_{i}.jpg")
#        ori_img_path = os.path.join(img_path, f"{image_name}_{i}.jpg")
#        role_image_path = os.path.join(role_dir,f"{role_name}.png")
#        generate_image(role_image_path,ori_img_path,tar_img_file1)
#        print(tar_img_file1)
