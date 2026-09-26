from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database import init_db

from .routes import router

app = FastAPI(

    title="FitBuddy – AI Fitness Plan Generator",

    description=(
        "AI-powered personalized fitness "
        "plan generator using FastAPI and Gemini."
    ),

    version="1.0.0"
)


app.mount(

    "/static",

    StaticFiles(
        directory=Path(__file__).resolve().parent.parent / "templates" / "static"
    ),

    name="static"
)


app.include_router(router)


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="/static/favicon.svg")


@app.on_event("startup")
def startup_event():

    init_db()