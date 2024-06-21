import fitz  # PyMuPDF
import openai
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
print(openai.api_key)

def chat_with_openai():
    print("You can start chatting with OpenAI. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        bot_response = response['choices'][0]['message']['content'].strip()
        print(f"OpenAI: {bot_response}")

if __name__ == "__main__":
    chat_with_openai()