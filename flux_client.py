import requests
import base64
import time
import argparse
import random
import os
import json
from openai import OpenAI
from tqdm.notebook import tqdm
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.0.11:7090/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


# 9节点0卡服务
#server_url = 'http://192.168.0.9:5000/inference'

# 9节点1卡服务
server_url = 'http://192.168.0.9:5001/inference'

# 9节点2卡服务
# server_url = 'http://192.168.0.9:5002/inference'

# 9节点3卡服务
# server_url = 'http://192.168.0.9:5003/inference'

# 14节点2卡服务
#server_url = 'http://192.168.0.14:5000/inference'

# 14节点3卡服务
#server_url = 'http://192.168.0.14:5000/inference'


def call_flux_server(prompt, use_lora=False):
    """调用Flux http生图服务

    Args:
        prompt(str): 描述
        use_lora(bool): 是否启用写实lora，目前只有人像使用写实lora

    Returns:
        服务返回

    """

    data = {'prompt': prompt, 'use_lora': use_lora}
    response = requests.post(server_url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text_path', type=str, default='/root/hanfubo/prompt_9_19.txt')
    parser.add_argument('--output_dir', type=str, default='/appsharedata/hanfubo/flux_res')
    args = parser.parse_args()
    
    text_path = args.text_path
    text_name = text_path.split('/')[-1].split('.')[0]
    assert text_path.endswith('.txt')
    with open(text_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    os.makedirs(f'{args.output_dir}/json', exist_ok=True)
    os.makedirs(f'{args.output_dir}/{text_name}', exist_ok=True)
    rand_lines = random.sample(lines, 100)
    data = {}
    for i, prompt in enumerate(rand_lines):
        # prompt = "White-washed windmills gently rotate against the sea's serene backdrop."
        use_lora = False
        chat_response = client.chat.completions.create(
            model="Qwen2-57b-A14-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"你现在是一个AI prompt判别器，请你判断以下prompt中是否有人物信息出现，返回内容只能是“是”或者“否”，不要输出无关内容。原始prompt：{prompt}"},
            ]
        )
        if chat_response.choices[0].message.content == '是':
            use_lora = True
            prompt = "Realistic，Asian"+ prompt
        s = time.time()
        result = call_flux_server(prompt, use_lora)
        e = time.time()
        if result is None:
            continue
        print("生成图片耗时:{}, prompt:[{}], 使用lora: [{}]".format(e - s, prompt, use_lora))
        data[f'{args.output_dir}/{text_name}/{str(i).zfill(6)}.png'] = {'time': e - s, 'prompt': prompt, 'use_lora': use_lora}
        # 将图片保存到test.png
        with open(f'{args.output_dir}/{text_name}/{str(i).zfill(6)}.png', 'wb') as f:
            f.write(base64.b64decode(result['image']))
        with open(f'{args.output_dir}/json/{text_name}.json', 'w') as file:
            json.dump(data, file, indent=4)
