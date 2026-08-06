# app.py
# AI Interview Assistant — FastAPI Application
# Production-ready with full routing, session management, and error handling.

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Request, Form, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
# pyrefly: ignore [missing-import]
from fastapi.templating import Jinja2Templates
# pyrefly: ignore [missing-import]
from fastapi.staticfiles import StaticFiles
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import random
import uuid
import os

from gemini import generate_questions, evaluate_answers

load_dotenv()

# ============================================================
# App Initialization
# ============================================================

app = FastAPI(
    title="InterviewGPT AI",
    description="AI Powered Interview Preparation Platform",
    version="2.0.0"
)

# CORS middleware (needed for production deployments)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# Templates
templates = Jinja2Templates(directory="templates")

# ============================================================
# In-memory session store
# In production, replace with Redis or a database.
# ============================================================

sessions = {}

QUESTIONS_PER_ROUND = 20


# ============================================================
# ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """Landing page."""
    try:
        return templates.TemplateResponse(
            "landing.html",
            {"request": request}
        )
    except Exception as e:
        print(f"[ERROR] Landing page: {e}")
        return HTMLResponse("<h1>Service temporarily unavailable. Please try again.</h1>", status_code=500)


# ============================================================
# FEATURE DETAIL PAGES
# ============================================================

@app.get("/features/ai-evaluation", response_class=HTMLResponse)
async def feature_ai_evaluation(request: Request):
    """AI Evaluation feature detail page."""
    return templates.TemplateResponse("feature_ai_evaluation.html", {"request": request})


@app.get("/features/job-roles", response_class=HTMLResponse)
async def feature_job_roles(request: Request):
    """20+ Job Roles feature detail page."""
    return templates.TemplateResponse("feature_job_roles.html", {"request": request})


@app.get("/features/instant-feedback", response_class=HTMLResponse)
async def feature_instant_feedback(request: Request):
    """Instant Feedback feature detail page."""
    return templates.TemplateResponse("feature_instant_feedback.html", {"request": request})


@app.get("/features/offline-evaluation", response_class=HTMLResponse)
async def feature_offline_evaluation(request: Request):
    """Offline Evaluation feature detail page."""
    return templates.TemplateResponse("feature_offline_evaluation.html", {"request": request})


@app.get("/features/technical-questions", response_class=HTMLResponse)
async def feature_technical_questions(request: Request):
    """Technical Questions feature detail page."""
    return templates.TemplateResponse("feature_technical_questions.html", {"request": request})


@app.get("/features/hr-questions", response_class=HTMLResponse)
async def feature_hr_questions(request: Request):
    """HR Questions feature detail page."""
    return templates.TemplateResponse("feature_hr_questions.html", {"request": request})


@app.post("/start-interview")
async def start_interview(
    role: str = Form(...),
    experience: str = Form(...)
):
    """
    Creates a new interview session.
    Generates a full question pool and selects the first round of 20.
    """
    try:
        session_id = str(uuid.uuid4())

        # Get full question pool (50+) for this role
        full_pool = generate_questions(role, experience)

        if not full_pool:
            full_pool = [
                "Tell me about yourself.",
                "Why are you interested in this role?",
                "What are your greatest strengths?",
                "Where do you see yourself in 5 years?",
                "Describe a challenging project you worked on.",
            ]

        random.shuffle(full_pool)

        # Select first round of questions
        first_round = full_pool[:QUESTIONS_PER_ROUND]
        remaining_pool = full_pool[QUESTIONS_PER_ROUND:]

        sessions[session_id] = {
            "role": role,
            "experience": experience,
            "questions": first_round,         # Current round's questions
            "answers": [],
            "full_pool": remaining_pool,       # Remaining unused questions
            "round": 1,
            "result": None,
            "all_completed": False,
        }

        return RedirectResponse(
            url=f"/interview/{session_id}",
            status_code=303
        )

    except Exception as e:
        print(f"[ERROR] start_interview: {e}")
        return RedirectResponse(url="/?error=start", status_code=303)


@app.get("/interview/{session_id}", response_class=HTMLResponse)
async def interview(request: Request, session_id: str):
    """Renders the interview page for the current round."""
    try:
        data = sessions.get(session_id)
        if not data:
            return RedirectResponse("/")

        return templates.TemplateResponse(
            "interview.html",
            {
                "request": request,
                "session_id": session_id,
                "role": data["role"],
                "experience": data.get("experience", ""),
                "questions": data["questions"],
                "round": data.get("round", 1),
            }
        )
    except Exception as e:
        print(f"[ERROR] interview page: {e}")
        return RedirectResponse("/")


@app.post("/submit/{session_id}")
async def submit_interview(session_id: str, request: Request):
    """
    Collects answers, runs AI/offline evaluation,
    stores results, and redirects to result page.
    """
    try:
        data = sessions.get(session_id)
        if not data:
            return RedirectResponse("/", status_code=303)

        form_data = await request.form()

        answers = [
            form_data.get(f"answer_{i}", "").strip()
            for i in range(len(data["questions"]))
        ]

        data["answers"] = answers

        # Evaluate with Gemini → offline fallback
        result = evaluate_answers(
            data["questions"],
            answers,
            data["role"]
        )

        data["result"] = result

        return RedirectResponse(
            url=f"/result/{session_id}",
            status_code=303
        )

    except Exception as e:
        print(f"[ERROR] submit_interview: {e}")
        return RedirectResponse("/", status_code=303)


@app.get("/result/{session_id}", response_class=HTMLResponse)
async def result(request: Request, session_id: str):
    """Renders the result page after interview evaluation."""
    try:
        data = sessions.get(session_id)
        if not data or not data.get("result"):
            return RedirectResponse("/")

        res = data["result"]
        remaining = data.get("full_pool", [])
        can_practice_more = len(remaining) >= QUESTIONS_PER_ROUND
        all_completed = data.get("all_completed", False)

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "session_id": session_id,
                "role": data["role"],
                "round": data.get("round", 1),
                "score": res.get("score", 0),
                "feedback": res.get("feedback", ""),
                "strengths": res.get("strengths", []),
                "improvements": res.get("improvements", []),
                "question_feedback": res.get("question_feedback", []),
                "can_practice_more": can_practice_more,
                "all_completed": all_completed,
            }
        )
    except Exception as e:
        print(f"[ERROR] result page: {e}")
        return RedirectResponse("/")


@app.get("/practice-more/{session_id}", response_class=HTMLResponse)
async def practice_more(request: Request, session_id: str):
    """
    Loads the next round of questions from the remaining pool.
    No questions repeat across rounds.
    If pool is exhausted, marks all_completed and shows completion on result page.
    """
    try:
        data = sessions.get(session_id)
        if not data:
            return RedirectResponse("/")

        remaining = data.get("full_pool", [])

        if len(remaining) < QUESTIONS_PER_ROUND:
            # Not enough questions for another full round — mark completed
            if len(remaining) == 0:
                # Absolutely no questions left — show completion on result page
                data["all_completed"] = True
                return RedirectResponse(
                    url=f"/result/{session_id}",
                    status_code=303
                )
            # Use whatever's left (partial round)
            next_questions = remaining
            new_remaining = []
        else:
            next_questions = remaining[:QUESTIONS_PER_ROUND]
            new_remaining = remaining[QUESTIONS_PER_ROUND:]

        data["questions"] = next_questions
        data["full_pool"] = new_remaining
        data["answers"] = []
        data["result"] = None
        data["all_completed"] = False
        data["round"] = data.get("round", 1) + 1

        return RedirectResponse(
            url=f"/interview/{session_id}",
            status_code=303
        )

    except Exception as e:
        print(f"[ERROR] practice_more: {e}")
        return RedirectResponse("/")

@app.get("/health")
async def health():
    """Health check endpoint for deployment platforms."""
    return {
        "status": "running",
        "service": "InterviewGPT AI",
        "version": "2.0.0"
    }



# ============================================================
# Global Exception Handler
# ============================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "landing.html",
        {"request": request},
        status_code=200
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception):
    return HTMLResponse(
        """
        <html>
        <head><title>InterviewGPT AI</title></head>
        <body style="background:#07132c;color:white;font-family:Poppins,sans-serif;
                     display:flex;justify-content:center;align-items:center;
                     min-height:100vh;text-align:center;">
          <div>
            <h1 style="font-size:42px;margin-bottom:16px;">Something went wrong</h1>
            <p style="color:#94a3b8;margin-bottom:32px;">
              The server encountered an unexpected error. Please try again.
            </p>
            <a href="/" style="background:linear-gradient(90deg,#2563eb,#9333ea);
               color:white;padding:14px 32px;border-radius:50px;text-decoration:none;
               font-weight:600;">Go Home</a>
          </div>
        </body>
        </html>
        """,
        status_code=500
    )