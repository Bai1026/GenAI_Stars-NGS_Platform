import openai
import os
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 全局变量来存储预设文本响应
preset_response = ""

def initialize_agent():
    global preset_response
    prompt = "This is a preset context to initialize the conversation with OpenAI."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 或其他支持的模型
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    preset_response = response['choices'][0]['message']['content'].strip()

# 初始化时发送预设文本
initialize_agent()

# def index(request):
#     return render(request, 'chatbot_app/index.html')

def index(request):
    global preset_response
    # return render(request, 'chatbot_app/index.html', {'preset_response': preset_response})
    return render(request, 'chatbot_app/index.html')


def chat(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或其他支持的模型
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        bot_response = response['choices'][0]['message']['content'].strip()
        return JsonResponse({"response": bot_response})
