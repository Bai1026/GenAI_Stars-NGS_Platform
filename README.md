# GenAI_Stars-NGS_Platform
- This is the platform for [GenAI Stars 2024](https://genaistars.org.tw/hackathon)
- For [Roche Taiwan](https://www.roche.com.tw/): Utilizing Generative AI to enhance public understanding of health insurance coverage for Next-Generation Sequencing (NGS) testing.
- We design a platform for:  
    1. Introduction
    2. Chatbot Platform (Fine-tune with the expertise)

## Demo Video

<p align="center">
  <a href="https://www.youtube.com/watch?v=P4eeqVuZfnQ">
    <img src="https://img.youtube.com/vi/P4eeqVuZfnQ/0.jpg" alt="Watch the video">
  </a>
</p>


## How to use
First, you need to install the package we need
```bash
pip install -r requirements.txt
```

Then you need to have the openai API key (we use gpt-3.5-turbo here)
```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

Lastly, run the Django server to open the website
```bash
python manage.py runserver
```

## Structure
```bash
├── NGS_Platform
│   ├── NGS_Platform
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── static
│   │   │   ├── css
│   │   │   ├── images
│   │   │   └── js
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── RAG
│   │   ├── dataset
│   │   │   ├── json
│   │   │   ├── pdf
│   │   │   ├── pdf_to_json.py
│   │   │   └── txt
│   │   └── initialize.py
│   ├── chatbot_app
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── home
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   └── templates
│       ├── chatbot_app
│       └── home
├── record
└── test_api.py
```

<!-- git rm --cached '*__pycache__'
git commit -m "Remove all __pycache__ files from tracking"
find . -name '__pycache__' -type f -delete
git push -->
