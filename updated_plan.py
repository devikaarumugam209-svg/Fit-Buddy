from google import genai

from .config import settings
from .gemini_generator import SYSTEM_SAFETY


def update_workout_plan(

    original_plan: str,

    feedback: str,

    goal: str,

    intensity: str

):

    if not settings.gemini_api_key:

        return (

            original_plan

            + "\n\n"
            + "-----------------------------\n"
            + "UPDATED PLAN\n"
            + "-----------------------------\n\n"

            + f"Feedback considered:\n{feedback}\n\n"

            + "The plan should be adjusted safely "
            "while keeping appropriate recovery."
        )


    client = genai.Client(

        api_key=settings.gemini_api_key
    )


    prompt = f"""

{SYSTEM_SAFETY}


Here is the original FitBuddy plan:

{original_plan}


User feedback:

{feedback}


Fitness goal:

{goal}


Intensity:

{intensity}


Create a revised 7-day fitness plan.

Apply the user's feedback.

Keep useful parts of the original plan.

Include at least one rest/recovery day.

Keep exercises safe and general.

Return only the revised plan.
"""


    response = client.models.generate_content(

        model=settings.workout_model,

        contents=prompt
    )


    return response.text.strip()