# AI Interview Preparation Assistant

This is an AI Interview Preparation Assistant developed to help students and job seekers practice interviews. Users can select their job role and experience level, answer interview questions, and get instant feedback on their performance.

## Live Demo

https://ai-interview-assistant-qvx8.onrender.com

## Features

- Practice technical and HR interview questions
- Support for 20+ job roles
- AI-based answer evaluation using Google Gemini
- Offline evaluation if AI is not available
- Performance score with strengths and improvement suggestions
- Practice more questions without repeating previous ones
- Simple and responsive user interface

## Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- FastAPI
- Jinja2

AI:
- Google Gemini API

Deployment:
- Render

Tools:
- VS Code
- Git
- GitHub

## Project Structure

```text
AI_Interview_Assistant/
│
├── app.py
├── gemini.py
├── requirements.txt
├── templates/
├── static/
├── .env
└── README.md
```

## How to Run the Project

Clone the repository

```bash
git clone https://github.com/saranyatripurari/AI_Interview_Assistant.git
```

Go to the project folder

```bash
cd AI_Interview_Assistant
```

Install the required packages

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Gemini API key

```text
GEMINI_API_KEY=your_api_key
```

Run the project

```bash
uvicorn app:app --reload
```

Open your browser and visit

```text
http://127.0.0.1:8000
```

## Future Improvements

- User login and registration
- Save interview history
- Download interview report as PDF
- Voice interview support
- More job roles
- Better analytics

## Author

Saranya Tripurari

Email: saranyatripurari@gmail.com

GitHub:
https://github.com/saranyatripurari

LinkedIn:
https://linkedin.com/in/saranyatripurari