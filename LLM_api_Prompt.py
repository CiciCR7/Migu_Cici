from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"  # 此处通常是OpenAI API密钥，该处设为空时，一般可能是调用本地部署的api
openai_api_base = "http://192.168.0.11:7090/v1"，# 设置 API 基础 URL。这里的地址 http://192.168.0.11:7090/v1 指向本地的 vLLM（大语言模型） API 服务器，而不是 OpenAI 官方的 API。

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)# 创建 OpenAI 类的一个实例 client，通过 api_key 和 base_url 参数指定使用的 API 密钥和基础 URL。client 是后续与 API 交互的对象。


fp = open('jieri.txt', 'w')
loop_times = 15

topic_list = ["节日装饰", "传统习俗", "家庭团聚", "节日氛围", "浪漫场景", "情侣互动", "爱情表达"]
for topic in topic_list:
    for i in range(loop_times):
        chat_response = client.chat.completions.create( # 
            #使用 client 对象的 chat.completions.create() 方法来调用大语言模型生成内容。该方法负责向 API 发出请求，并获取聊天或完成任务的响应。
            model="Qwen2-57b-A14-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"你现在是一个AI绘画prompt生成器，请你生成20条主题为'{topic}'的prompt，要求prompt描绘的场景为写实风格，构图良好，高清，摄影作品级别。且符合中国国内场景。直接用英文输出。每一条prompt直接用换行符分割，不要用数字标记"},
            ]
        )
        print("Chat response:", chat_response)
        fp.write(chat_response.choices[0].message.content.replace('\n\n', '\n'))
        fp.flush()# ：强制将缓冲区的数据写入文件，确保生成内容即时写入而不是等待缓冲区满时才写入。

fp.close()
