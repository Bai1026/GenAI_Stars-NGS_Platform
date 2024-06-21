# import openai
# import os
# from django.shortcuts import render
# from django.http import JsonResponse
# from dotenv import load_dotenv

# # 加载环境变量
# load_dotenv()
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # 全局变量来存储预设文本响应
# preset_response = ""

# def initialize_agent():
#     global preset_response
#     prompt = "This is a preset context to initialize the conversation with OpenAI."

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",  # 或其他支持的模型
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#     preset_response = response['choices'][0]['message']['content'].strip()

# # 初始化时发送预设文本
# initialize_agent()

# # def index(request):
# #     return render(request, 'chatbot_app/index.html')

# def index(request):
#     global preset_response
#     # return render(request, 'chatbot_app/index.html', {'preset_response': preset_response})
#     return render(request, 'chatbot_app/index.html')


# def chat(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('message')
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # 或其他支持的模型
#             messages=[
#                 {"role": "user", "content": user_input}
#             ]
#         )
#         bot_response = response['choices'][0]['message']['content'].strip()
#         return JsonResponse({"response": bot_response})


from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import json
import openai
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def index(request):
    return render(request, 'chatbot_app/index.html')

def chat(request):
    if request.method == 'POST':
        try:
            data = request.POST.get('message')
            user_message = data

            if not user_message:
                return HttpResponseBadRequest("Message is required")

            # 调用 OpenAI API 生成回复
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 或 "gpt-4"
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            bot_response = response.choices[0].message['content'].strip()

            return JsonResponse({'response': bot_response})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest("Invalid request method")