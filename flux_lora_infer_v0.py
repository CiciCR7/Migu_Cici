import torch
from diffusers import FluxPipeline
import json
import os
import sys

pipe = FluxPipeline.from_pretrained("/sharedata/duzongcai/model_weights/FLUX.1-dev", torch_dtype=torch.float16)
pipe.load_lora_weights("/sharedata/duzongcai/model_weights/flux-RealismLora",weight_name="lora.safetensors")
pipe.fuse_lora(lora_scale=1.0)
pipe.to("cuda")
filename = "20240910-105638_1000.json"
with open(filename, 'r', encoding='utf-8') as file:
    data = json.load(file)

for filename, prompt in data.items():
    image = pipe(prompt, 
                 num_inference_steps=50, 
                 guidance_scale=4.0,
                 width=720, height=1280,
                ).images[0]
    image.save(f"data/flux-RealismLora/{filename}.png")
