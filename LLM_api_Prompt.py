from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://192.168.0.11:7090/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


fp = open('jieri.txt', 'w')
loop_times = 15

topic_list = ["节日装饰", "传统习俗", "家庭团聚", "节日氛围", "浪漫场景", "情侣互动", "爱情表达"]
for topic in topic_list:
    for i in range(loop_times):
        chat_response = client.chat.completions.create(
            model="Qwen2-57b-A14-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"你现在是一个AI绘画prompt生成器，请你生成20条主题为'{topic}'的prompt，要求prompt描绘的场景为写实风格，构图良好，高清，摄影作品级别。且符合中国国内场景。直接用英文输出。每一条prompt直接用换行符分割，不要用数字标记"},
            ]
        )
        print("Chat response:", chat_response)
        fp.write(chat_response.choices[0].message.content.replace('\n\n', '\n'))
        fp.flush()

fp.close()
