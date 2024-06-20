from django.shortcuts import render
from django.http import JsonResponse
import openai

openai.api_key = 'YOUR_API_KEY'

def index(request):
    return render(request, 'chatbot_app/index.html')

def chat(request):
    if request.method == 'POST':
        user_input = request.POST.get('message')
        response = openai.Completion.create(
            engine="davinci-codex",  # 或其他模型
            prompt=user_input,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
        return JsonResponse({"response": bot_response})
