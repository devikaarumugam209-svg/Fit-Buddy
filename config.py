import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "FitBuddy")

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./fitbuddy.db"
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    )

    workout_model: str = os.getenv(
        "GEMINI_WORKOUT_MODEL",
        "gemini-3.8-flash"
    )

    tip_model: str = os.getenv(
        "GEMINI_TIP_MODEL",
        "gemini-3.5-flash-lite"
    )


settings = Settings()