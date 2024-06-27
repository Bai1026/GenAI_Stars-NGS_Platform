# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponseBadRequest
# import logging
# import openai
# import os
# from dotenv import load_dotenv

# import json

# # 加载环境变量
# load_dotenv()
# openai.api_key = os.getenv('OPENAI_API_KEY')

# # 全局变量来存储用户信息
# user_info = {}

# # 配置日志记录
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s %(levelname)s %(message)s',
#     handlers=[
#         logging.FileHandler("chatbot_app.log"),
#         logging.StreamHandler()
#     ]
# )

# logger = logging.getLogger(__name__)

# def index(request):
#     return render(request, 'chatbot_app/index.html')

# def submit_user_info(request):
#     global user_info
#     if request.method == 'POST':
#         try:
#             # original code -> use request.POST.get() to get form data -> not working
#             # assume the form data is sent as key-value pairs

#             # user_info['age'] = request.POST.get('age', 'N/A')
#             # user_info['education'] = request.POST.get('education', 'N/A')
#             # user_info['occupation'] = request.POST.get('occupation', 'N/A')
#             # user_info['language'] = request.POST.get('language', 'N/A')
#             # logger.info(f"User info submitted: {user_info}")


#             # new code -> use request.body to get JSON data -> since we use fetch API with AJAX request to send data
#             # assume the form data is sent as JSON data

#             data = json.loads(request.body)
#             user_info['age'] = data.get('age', 'N/A')
#             user_info['education'] = data.get('education', 'N/A')
#             user_info['occupation'] = data.get('occupation', 'N/A')
#             user_info['language'] = data.get('language', 'N/A')
#             logger.info(f"User info submitted: {user_info}")
#             return JsonResponse({'status': 'success'})
#         except json.JSONDecodeError:
#             logger.error("Failed to decode JSON from request body")
#             return HttpResponseBadRequest("Invalid JSON format")
#     return HttpResponseBadRequest("Invalid request method")

# def chat(request):
#     global user_info
#     if request.method == 'POST':
#         try:
#             user_message = request.POST.get('message')

#             if not user_message:
#                 return HttpResponseBadRequest("Message is required")

#             # 使用用户信息作为初始上下文
#             initial_prompt = f"此用戶資訊為： 年齡: {user_info.get('age')}, 教育程度: {user_info.get('education')}, 職業: {user_info.get('occupation')}, 語言: {user_info.get('language')}. 請根據此用戶資訊使用適合的術語去介紹NGS給用戶。如果沒有提及語言，預設即為中文。"
#             full_message = initial_prompt + "\n\n" + user_message

#             # 记录传递给模型的消息
#             logger.info(f"Full message to model: {full_message}")

#             # 调用 OpenAI API 生成回复
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",  # 或 "gpt-4"
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": full_message}
#                 ]
#             )
#             bot_response = response['choices'][0]['message']['content'].strip()

#             # 记录生成的回复
#             logger.info(f"Bot response: {bot_response}")

#             return JsonResponse({'response': bot_response})

#         except Exception as e:
#             logger.error(f"Error during chat: {str(e)}")
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return HttpResponseBadRequest("Invalid request method")


import os
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(__file__), "google_cloud_api.json")

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import logging
import openai
import os
from dotenv import load_dotenv

import json
from google.cloud import speech
import io

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# 全局变量来存储用户信息
user_info = {}

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("chatbot_app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'chatbot_app/index.html')

def submit_user_info(request):
    global user_info
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_info['age'] = data.get('age', 'N/A')
            user_info['education'] = data.get('education', 'N/A')
            user_info['occupation'] = data.get('occupation', 'N/A')
            user_info['language'] = data.get('language', 'N/A')
            logger.info(f"User info submitted: {user_info}")
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            logger.error("Failed to decode JSON from request body")
            return HttpResponseBadRequest("Invalid JSON format")
    return HttpResponseBadRequest("Invalid request method")

def transcribe_speech(audio_file):
    client = speech.SpeechClient()
    with io.open(audio_file, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="zh-CN",  # 根据需要设置语言
    )
    response = client.recognize(config=config, audio=audio)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript
    return transcript

def chat(request):
    global user_info
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message')

            if not user_message and 'audio' in request.FILES:
                audio_file = request.FILES['audio']
                user_message = transcribe_speech(audio_file)
                if not user_message:
                    return HttpResponseBadRequest("Audio transcription failed")

            if not user_message:
                return HttpResponseBadRequest("Message is required")

            # 使用用户信息作为初始上下文
            initial_prompt = f"此用戶資訊為： 年齡: {user_info.get('age')}, 教育程度: {user_info.get('education')}, 職業: {user_info.get('occupation')}, 語言: {user_info.get('language')}. 請根據此用戶資訊使用適合的術語去介紹NGS給用戶。如果沒有提及語言，預設即為中文。"
            full_message = initial_prompt + "\n\n" + user_message

            # 记录传递给模型的消息
            logger.info(f"Full message to model: {full_message}")

            # 调用 OpenAI API 生成回复
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 或 "gpt-4"
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": full_message}
                ]
            )
            bot_response = response.choices[0].message['content'].strip()

            # 记录生成的回复
            logger.info(f"Bot response: {bot_response}")

            return JsonResponse({'response': bot_response})

        except Exception as e:
            logger.error(f"Error during chat: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return HttpResponseBadRequest("Invalid request method")

