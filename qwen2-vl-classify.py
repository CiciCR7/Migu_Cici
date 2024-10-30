# 给图片进行场景打标
import os
import torch
import argparse
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
import shutil
import json  # 引入json模块

# Load the model
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct", torch_dtype="auto", device_map="auto"
)
print(model.dtype)

processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")

# Define category dictionary
categories = {
    'Sports': 0,
    'Music': 0,
    'Entertainment': 0,
    'Variety Shows': 0,
    'Movies': 0,
    'TV Series': 0,
    'Games': 0,
    'Travel': 0,
    'Humanities': 0,
    'Lifestyle': 0,
    'Fashion': 0,
    'Food': 0,
    'Scenery': 0,
    'Knowledge': 0,
    'Finance': 0,
    'Technology': 0,
    'Automobiles': 0,
    'Curiosity': 0,
    'News': 0,
    'Military': 0,
    'Documentary': 0,
    'Anime': 0,
    'ACG': 0,
    'Parenting': 0,
    'Comedy': 0,
    'Dance': 0,
    'General': 0,
}

def classify_images_in_folder(folder_path, output_path):
    for category in categories.keys():
        out_category_path = os.path.join(output_path, category)
        os.makedirs(out_category_path, exist_ok=True)
    print("分类文件夹创建完成！分类成功的会复制到结果文件夹中的对应类别文件夹...\n")
    damaged_files = []  # List to keep track of damaged files
    total_images = 0  # 统计总图片数

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            total_images += 1  # 每处理一张图片，计数加一
            image_path = os.path.join(folder_path, filename)

            # Try to open the image and handle any errors
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
                        {"type": "text", "text": "You are an image scene category classification assistant. Your task is to categorize images into one of the following categories: Sports, Music, Entertainment, Variety Shows, Movies, TV Series, Games, Travel, Humanities, Lifestyle, Fashion, Food, Scenery, Knowledge, Finance, Technology, Automobiles, Curiosity, News, Military, Documentary, Anime, ACG, Parenting, Comedy, Dance, General. First, think step by step about the content of the image and determine which category it fits best. After careful consideration, provide only the single best-matching category from the list, without any additional information or explanation."},
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
            category = output_text[0]
            print(f"Image: {filename} - Category: {category}")

            if category in categories:
                categories[category] += 1
                out_category_path = os.path.join(output_path, category)
                shutil.copy(image_path, out_category_path)
                print(f"图片{filename}已复制到文件夹{out_category_path}\n")
            else:
                print(f"类别{category}未找到，跳过图片{filename}\n")

    # Output the category counts
    print("\nCategory Counts:")
    for category, count in categories.items():
        print(f"{category}: {count}")

    # Save statistics to a JSON file
    statistics = {
        "total_images": total_images,
        "category_counts": categories
    }

    with open(os.path.join(output_path, 'category_statistics.json'), 'w') as f:
        json.dump(statistics, f, ensure_ascii=False, indent=4)
    print(f"\n统计信息已保存到 {output_path}/category_statistics.json")

    # Optionally, report damaged files
    if damaged_files:
        print("\nDamaged Files:")
        for damaged_file in damaged_files:
            print(damaged_file)

if __name__ == "__main__":
    # Command line argument parsing
    parser = argparse.ArgumentParser(description="Classify images in a folder.")
    parser.add_argument("--folder_path", type=str, help="Path to the folder containing images.")
    parser.add_argument("--output_path", type=str, help="Path to the folder containing classified images.")
    args = parser.parse_args()

    classify_images_in_folder(args.folder_path, args.output_path)

# import os
# import torch
# import argparse
# from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
# from qwen_vl_utils import process_vision_info
# from PIL import Image
# import shutil

# # Load the model
# model = Qwen2VLForConditionalGeneration.from_pretrained(
#     "Qwen/Qwen2-VL-7B-Instruct", torch_dtype="auto", device_map="auto"
# )

# processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")

# # Define category dictionary
# categories = {
#     'Sports': 0,
#     'Music': 0,
#     'Entertainment': 0,
#     'Variety Shows': 0,
#     'Movies': 0,
#     'TV Series': 0,
#     'Games': 0,
#     'Travel': 0,
#     'Humanities': 0,
#     'Lifestyle': 0,
#     'Fashion': 0,
#     'Food': 0,
#     'Scenery': 0,
#     'Knowledge': 0,
#     'Finance': 0,
#     'Technology': 0,
#     'Automobiles': 0,
#     'Curiosity': 0,
#     'News': 0,
#     'Military': 0,
#     'Documentary': 0,
#     'Anime': 0,
#     'ACG': 0,
#     'Parenting': 0,
#     'Comedy': 0,
#     'Dance': 0,
#     'General': 0,
# }

# def classify_images_in_folder(folder_path, output_path):
#     for category in categories.keys():
#         out_category_path = os.path.join(output_path, category)
#         os.makedirs(out_category_path, exist_ok=True)
#     print("分类文件夹创建完成！分类成功的会复制到结果文件夹中的对应类别文件夹...\n")
#     damaged_files = []  # List to keep track of damaged files
#     for filename in os.listdir(folder_path):
#         if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
#             image_path = os.path.join(folder_path, filename)

#             # Try to open the image and handle any errors
#             try:
#                 with Image.open(image_path) as image:
#                     image.load()  # Force loading the image
#                     image = image.convert("RGB")  # Convert to RGB
#             except (IOError, SyntaxError, AttributeError) as e:
#                 print(f"Skipping damaged file: {image_path} - Error: {e}")
#                 damaged_files.append(image_path)  # Record the damaged file
#                 continue  # Skip to the next file

#             # Prepare the messages for inference
#             messages = [
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "image",
#                             "image": image,
#                         },
#                         {"type": "text", "text": "You are an image scene category classification assistant. Your task is to categorize images into one of the following categories: Sports, Music, Entertainment, Variety Shows, Movies, TV Series, Games, Travel, Humanities, Lifestyle, Fashion, Food, Scenery, Knowledge, Finance, Technology, Automobiles, Curiosity, News, Military, Documentary, Anime, ACG, Parenting, Comedy, Dance, General. First, think step by step about the content of the image and determine which category it fits best. After careful consideration, provide only the single best-matching category from the list, without any additional information or explanation."},
#                     ],
#                 }
#             ]

#             # Preparation for inference
#             text = processor.apply_chat_template(
#                 messages, tokenize=False, add_generation_prompt=True
#             )
#             image_inputs, video_inputs = process_vision_info(messages)
#             inputs = processor(
#                 text=[text],
#                 images=image_inputs,
#                 videos=video_inputs,
#                 padding=True,
#                 return_tensors="pt",
#             )
#             inputs = inputs.to("cuda")

#             # Inference: Generation of the output
#             generated_ids = model.generate(**inputs, max_new_tokens=128)
#             generated_ids_trimmed = [
#                 out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
#             ]
#             output_text = processor.batch_decode(
#                 generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
#             )

#             # Get the category and update the count
#             category = output_text[0]
#             print(f"Image: {filename} - Category: {category}")

#             if category in categories:
#                 categories[category] += 1
#                 out_category_path = os.path.join(output_path,category)
#                 shutil.copy(image_path, out_category_path)
#                 print(f"图片{filename}已复制到文件夹{out_category_path}\n")
#             else:
#                 print(f"类别{category}未找到，跳过图片{filename}\n")
                

#     # Output the category counts
#     print("\nCategory Counts:")
#     for category, count in categories.items():
#         print(f"{category}: {count}")

#     # Optionally, report damaged files
#     if damaged_files:
#         print("\nDamaged Files:")
#         for damaged_file in damaged_files:
#             print(damaged_file)

# if __name__ == "__main__":
#     # Command line argument parsing
#     parser = argparse.ArgumentParser(description="Classify images in a folder.")
#     parser.add_argument("--folder_path", type=str, help="Path to the folder containing images.")
#     parser.add_argument("--output_path", type=str, help="Path to the folder containing classified images.")
#     args = parser.parse_args()

#     classify_images_in_folder(args.folder_path, args.output_path)
