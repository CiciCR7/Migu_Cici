# Migu_Cici
记录该工作时期的代码
1.CLIP中，clip_match_move.py是计算图片之间的相似度，保留相似度高的一组图片中一张图片，简单作用为图片素材库去重
2、fluxclient.py，调用LLM api来实现判别prompt中是否出现人物信息，如有人物，在调用flux模型生成图片过程中加入lora模型。
