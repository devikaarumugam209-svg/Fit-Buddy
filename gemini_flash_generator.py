from google import genai

from .config import settings


def fallback_tip(goal):

    tips = {

        "weight loss":
        "Choose balanced meals with vegetables or fruit, protein-rich foods, whole grains, and water. Avoid extreme dieting.",

        "muscle gain":
        "Include a protein-rich food with regular meals and allow enough recovery between harder workouts.",

        "general wellness":
        "Stay hydrated, eat varied foods, sleep regularly, and choose enjoyable daily movement.",

        "flexibility":
        "Combine gentle mobility exercises with normal balanced meals, hydration, and adequate rest."
    }


    return tips.get(

        goal.lower(),

        "Focus on balanced meals, hydration, regular movement, and enough sleep."
    )


def generate_nutrition_tip_with_flash(
    goal: str
):

    if not settings.gemini_api_key:

        return fallback_tip(goal)


    client = genai.Client(

        api_key=settings.gemini_api_key
    )


    prompt = f"""

Give one concise nutrition or recovery
tip for a fitness user.

Fitness goal:

{goal}


The response should:

• Be practical
• Be easy to understand
• Be 2–4 sentences
• Avoid extreme diets
• Avoid dangerous advice
• Avoid medical claims
"""


    response = client.models.generate_content(

        model=settings.tip_model,

        contents=prompt
    )


    return response.text.strip()