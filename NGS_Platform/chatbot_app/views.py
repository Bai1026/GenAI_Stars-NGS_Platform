import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import logging
import openai
from dotenv import load_dotenv
import json
import whisper
import tempfile


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

user_info = {}

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
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in audio_file.chunks():
            temp_file.write(chunk)
        temp_file_path = temp_file.name

    model = whisper.load_model("base")
    result = model.transcribe(temp_file_path)
    
    os.remove(temp_file_path)
    
    return result['text']


def get_initial_prompt(user_info):
    age = user_info.get('age')
    education = user_info.get('education')
    occupation = user_info.get('occupation')
    language = user_info.get('language', '中文')

    # 基本的初始提示
    initial_prompt = f"此用戶資訊為： 年齡: {age}, 教育程度: {education}, 職業: {occupation}, 語言: {language}。"

    # 根据条件追加内容
    if age != 'N/A' and (int(age) < 18 | int(age) > 65):
        initial_prompt += "請用淺顯易懂的語言介紹什麼是NGS技術，並解釋其基本原理。"

    if education in ['小學', '國中', '高中', 'elementary', 'junior high', 'senior high']:
        initial_prompt += "請用淺顯易懂的語言介紹NGS技術，並解釋其基本原理。"

    if occupation in ['醫生', '醫療人員', '教授', 'doctor', 'professor', 'medical staff']:
        initial_prompt += "請詳細介紹NGS技術的醫學應用及其在研究中的重要性。"

    if '請用淺顯易懂的語言介紹' not in initial_prompt and '詳細介紹' not in initial_prompt:
        initial_prompt += "請根據此用戶資訊使用適合的術語去介紹NGS給用戶。如果沒有提及語言，預設即為中文，若有請用用戶語言回答。"

    return initial_prompt


def chat(request):
    global user_info
    if request.method == 'POST':
        try:
            user_message = request.POST.get('message')
            transcription = None
            logger.info(f"Received message: {user_message}")
            if not user_message and 'audio' in request.FILES:
                audio_file = request.FILES['audio']
                logger.info(f"Received audio file: {audio_file.name}")
                transcription = transcribe_speech(audio_file)
                user_message = transcription
                if not user_message:
                    return HttpResponseBadRequest("Audio transcription failed")

            if not user_message:
                logger.warning("No message provided")
                return HttpResponseBadRequest("Message is required")

            # initial_prompt = f"此用戶資訊為： 年齡: {user_info.get('age')}, 教育程度: {user_info.get('education')}, 職業: {user_info.get('occupation')}, 語言: {user_info.get('language')}. 請根據此用戶資訊使用適合的術語去介紹NGS給用戶。如果沒有提及語言，預設即為中文。"
            initial_prompt = get_initial_prompt(user_info)
            full_message = initial_prompt + "\n\n" + user_message

            logger.info(f"Full message to model: {full_message}")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": full_message}
                ]
            )
            bot_response = response['choices'][0]['message']['content'].strip()

            logger.info(f"Bot response: {bot_response}")

            return JsonResponse({'response': bot_response, 'transcription': transcription})

        except Exception as e:
            logger.error(f"Error during chat: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        logger.warning("Invalid request method")
        return HttpResponseBadRequest("Invalid request method")
