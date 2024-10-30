# 区分欧美人和亚洲人，给图片进行打标签

import os
import torch
import argparse
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
import shutil
import json  # 引入json模块
import time

# Load the model
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct", torch_dtype="auto", device_map="auto"
)
print(model.dtype)

processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")



def classify_images_in_folder(folder_path, output_path):
    # 新建两个结果文件夹
    Foreigners_path = output_path + '/Foreigners'
    Asians_path = output_path + '/Asians'
    total_images = 0
    max_images = 1000
    
    os.makedirs(Foreigners_path, exist_ok=True)
    os.makedirs(Asians_path, exist_ok = True)


    result_file = open(os.path.join(output_path, 'classify_people_result.txt'), 'w')
    
    for filename in sorted(os.listdir(folder_path)):
        if total_images > max_images:
            break
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            total_images += 1  # 每处理一张图片，计数加一
            image_path = os.path.join(folder_path, filename)

            # Try to open the image and handle any errors
            # 记录处理开始时间
            start_time = time.time()
            try:
                with Image.open(image_path) as image:
                    image.load()  # Force loading the image
                    image = image.convert("RGB")  # Convert to RGB
            except (IOError, SyntaxError, AttributeError) as e:
                print(f"Skipping damaged file: {image_path} - Error: {e}")
                damaged_files.append(image_path)  # Record the damaged file
                continue  # Skip to the next file

            # Prepare the messages for inference
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "image": image,
                        },
                        # {"type": "text", "text": "You are now a tool for distinguishing between Asians and Westerners. \
                        # Follow these steps to analyze the image:\
                        # 1.Carefully examine the image for any individuals.\
                        # 2.Identify the ethnicity of each person present.\
                        # 3.If you find any Westerners in the image, output 1.\
                        # 4.If there are no Westerners or if there are only Asians, output 0.\
                        # Please provide the answer directly based on your analysis."}
                        {"type": "text", "text": "Please analyze the image and output 1 if there are any Westerners present. If there are only Asians or no individuals, output 0. Provide the answer directly without any additional information."},
                    ],
                }
            ]

            # Preparation for inference
            text = processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            image_inputs, video_inputs = process_vision_info(messages)
            inputs = processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt",
            )
            inputs = inputs.to("cuda")

            # Inference: Generation of the output
            generated_ids = model.generate(**inputs, max_new_tokens=128)
            generated_ids_trimmed = [
                out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            output_text = processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )

            # Get the category and update the count
            category = output_text[0].strip() #去除可能的空格和特殊符号
            print(f"Image: {filename} - Category: {category}")
            result_file.write(f"{image_path} {category}\n")
            
            # 记录处理结束时间并计算时间差
            end_time = time.time()
            processing_time = end_time - start_time
            # 打印处理时间
            print(f"Processing time for {filename}: {processing_time:.2f} seconds")

            # 强制刷新缓存
            result_file.flush()  
            if category == '1':
                shutil.copy(image_path,Foreigners_path)
            else:
                shutil.copy(image_path, Asians_path)
    # 处理完所有图片后关闭
    result_file.close()

            

if __name__ == "__main__":
    # Command line argument parsing
    parser = argparse.ArgumentParser(description="Classify images in a folder.")
    parser.add_argument("--folder_path", type=str, help="Path to the folder containing images.")
    parser.add_argument("--output_path", type=str, help="Path to the folder containing classified images.")
    args = parser.parse_args()

    classify_images_in_folder(args.folder_path, args.output_path)
