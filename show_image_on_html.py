import os
from jinja2 import Environment, BaseLoader
import json

# 设定文件夹和文件路径
# original_folder_1 = "/ssd1/work/hanfubo/data/human_test/imgs"
# original_folder = "http://10.127.2.16:8444/data/human_test/imgs"
# mask_folder = "http://10.127.2.16:8444/data/human_test/mask"
# merge_folder = "http://10.127.2.16:8444/data/week_eval/pc_edit_data/bg_alter_2024-07-15_2024-07-21/merge/"
json_file_path = "/appsharedata/wangqiqi/flux_res/json/2-zhuti.json"
bianji_res_v1_path = "http://cloud-14-8444.vip.migu.cn:8888/appsharedata/wangqiqi/flux_res/2-zhuti/"
bianji_res_v2_path = "http://cloud-14-8444.vip.migu.cn:8888/data/flux-RealismLora"
bianji_res_v3_path = "http://cloud-14-8444.vip.migu.cn:8888/data/FLUX.1-dev-LoRA-add-details"
bianji_res_v4_path = "http://cloud-14-8444.vip.migu.cn:8888/data/FilmPortrait"
bianji_res_v5_path = "http://cloud-14-8444.vip.migu.cn:8888/data/AWPortrait-FL"

# with open(txt_file_path, 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#     data = [line.strip().split(',') for line in lines]
# print(data)

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

res_data = []

# 为每一行生成对应的图片路径
# image_files = os.listdir(original_folder_1)
# for i, file in enumerate(image_files):
#     if file == ".ipynb_checkpoints":
#         continue
    # original_image = file
    # original_name_without_extension = os.path.splitext(original_image)[0]
    # img_file = os.path.join(original_folder, original_image)
    # mask_file = os.path.join(mask_folder, original_image)
    # merge_file = os.path.join(merge_folder, original_image)

    # res_row = [f"线上_{i+1}", img_file, mask_file]
    # for j in range(4):
    #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # for j in range(15):
    #     prompt = data[j][1]
    #     print(prompt)
    #     res_row = [f"{i*15+j}", img_file,mask_file,prompt]
    #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    #     res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_{j}.jpg"))
    #     res_data.append(res_row)
    # # res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_1.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_2.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_3.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_4.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_4.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)
i = 0
for filename, prompt_all in data.items():
    prompt = prompt_all["prompt"]
    lora_bool =  prompt_all["use_lora"]
    res_row = [filename, prompt,lora_bool]
    print(prompt)
    res_row.append(os.path.join(bianji_res_v1_path, filename))
    print(os.path.join(bianji_res_v1_path, filename))
    # res_row.append(os.path.join(bianji_res_v2_path, f"{filename}.png"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{filename}.png"))
    # res_row.append(os.path.join(bianji_res_v4_path, f"{filename}.png"))
    # res_row.append(os.path.join(bianji_res_v5_path, f"{filename}.png"))
    # for j in range(4):
    #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_0.jpeg"))
    # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_1.jpeg"))
    # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_2.jpeg"))
    # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_3.jpeg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    res_data.append(res_row)
    # res_row = [f"垫图_{i+1}", img_file,mask_file]
    # for j in range(15):
    #     res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_{j}.jpg"))
    # # for j in range(4):
    # #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_0.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_1.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_2.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_3.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)

    # res_row = [f"sdxl_brushnet_{i+1}", img_file,mask_file]
    # for j in range(15):
    #     res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_{j}.jpg"))
    # # for j in range(4):
    # #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_0.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_1.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_2.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v2_path, f"{original_name_without_extension}_3.jpeg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)

    # res_row = [f"guidance_scale_18_{i+1}", img_file, merge_file, prompt]
    # # for j in range(4):
    # #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)

    # res_row = [f"guidance_scale_21_{i+1}", img_file, merge_file, prompt]
    # # # for j in range(4):
    # # #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # res_row.append(os.path.join(bianji_res_v4_path, f"{original_name_without_extension}_0.jpg"))
    # res_row.append(os.path.join(bianji_res_v4_path, f"{original_name_without_extension}_1.jpg"))
    # res_row.append(os.path.join(bianji_res_v4_path, f"{original_name_without_extension}_2.jpg"))
    # res_row.append(os.path.join(bianji_res_v4_path, f"{original_name_without_extension}_3.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)

    # res_row = [f"guidance_scale_24_{i+1}", img_file, merge_file, prompt]
    # # # for j in range(4):
    # # #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # res_row.append(os.path.join(bianji_res_v5_path, f"{original_name_without_extension}_0.jpg"))
    # res_row.append(os.path.join(bianji_res_v5_path, f"{original_name_without_extension}_1.jpg"))
    # res_row.append(os.path.join(bianji_res_v5_path, f"{original_name_without_extension}_2.jpg"))
    # res_row.append(os.path.join(bianji_res_v5_path, f"{original_name_without_extension}_3.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)

    # res_row = [f"guidance_scale_27_{i+1}", img_file, merge_file, prompt]
    # # # for j in range(4):
    # # #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # res_row.append(os.path.join(bianji_res_v6_path, f"{original_name_without_extension}_0.jpg"))
    # res_row.append(os.path.join(bianji_res_v6_path, f"{original_name_without_extension}_1.jpg"))
    # res_row.append(os.path.join(bianji_res_v6_path, f"{original_name_without_extension}_2.jpg"))
    # res_row.append(os.path.join(bianji_res_v6_path, f"{original_name_without_extension}_3.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)

    # res_row = [f"guidance_scale_30_{i+1}", img_file, merge_file, prompt]
    # # # for j in range(4):
    # # #     res_row.append(os.path.join(bianji_res_v1_path, f"{original_name_without_extension}_{j}.jpg"))
    # res_row.append(os.path.join(bianji_res_v7_path, f"{original_name_without_extension}_0.jpg"))
    # res_row.append(os.path.join(bianji_res_v7_path, f"{original_name_without_extension}_1.jpg"))
    # res_row.append(os.path.join(bianji_res_v7_path, f"{original_name_without_extension}_2.jpg"))
    # res_row.append(os.path.join(bianji_res_v7_path, f"{original_name_without_extension}_3.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_0.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_1.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_2.jpg"))
    # # # res_row.append(os.path.join(bianji_res_v3_path, f"{original_name_without_extension}_3.jpg"))
    # res_data.append(res_row)

# Jinja2模板
template_string = """
<!DOCTYPE html>
<html>
<head>
    <title>Images</title>
    <meta charset="utf-8">
    <style>
        td:nth-child(1), td:nth-child(1) {
            width: 100px;  # 调整这个数值以改变第二列的宽度
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
</head>
<body>
    <table border="1">
        {% for row in data %}
        <tr>
            <th>文件名</th>
            <th>prompt</th>
             <th>是否使用lora</th>
            <th>图像</th>

        </tr>
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
            <td>{{ row[2] }}</td>
            <td><img src="{{ row[3] }}" alt="{{ row[3] }}" width="250"></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

template = Environment(loader=BaseLoader).from_string(template_string)


bianji_html_path = "/appsharedata/wangqiqi/flux_res/test.html"
with open(bianji_html_path, "w", encoding='utf-8') as f:
    f.write(template.render(data=res_data))
