from google import genai

from .config import settings


SYSTEM_SAFETY = """
You are the fitness-planning component of FitBuddy.

Create general wellness guidance, not medical diagnosis or treatment.

Keep plans age-appropriate and conservative.

Do not recommend:
- starvation
- extreme dieting
- dehydration
- dangerous exercise challenges
- performance-enhancing drugs
- unsafe exercise
- punishment exercise

Always include recovery and rest.

If the user reports pain, injury, dizziness,
fainting, chest pain, or unusual symptoms,
recommend stopping the activity and seeking
appropriate professional help.
"""


def fallback_plan(
    username,
    goal,
    intensity
):

    return f"""
FITBUDDY 7-DAY FITNESS PLAN

Name: {username}

Goal: {goal}

Intensity: {intensity}


DAY 1 – FULL BODY

Warm-up:
5–10 minutes of easy walking and mobility.

Main workout:
• Bodyweight squats – 2 × 8–12
• Wall push-ups – 2 × 8–12
• Glute bridges – 2 × 10–15
• Easy walking – 10–15 minutes

Cool-down:
5 minutes gentle stretching.


DAY 2 – CARDIO + MOBILITY

Warm-up:
5 minutes easy movement.

Main workout:
• Comfortable walking or cycling – 20–30 minutes
• Gentle mobility exercises

Cool-down:
5 minutes.


DAY 3 – RECOVERY

• Gentle walking – 15–20 minutes
• Light stretching
• Focus on hydration and sleep


DAY 4 – FULL BODY

Warm-up:
5–10 minutes.

Main workout:
• Sit-to-stand – 2 × 8–12
• Wall push-ups – 2 × 8–12
• Bird-dog – 2 × 6–10 each side
• Easy walking – 10–15 minutes

Cool-down:
5 minutes.


DAY 5 – CARDIO + CORE

Warm-up:
5 minutes.

Main workout:
• Comfortable cardio – 20–25 minutes
• Dead bug – 2 × 6–10 each side
• Gentle core work

Cool-down:
5 minutes.


DAY 6 – LIGHT ACTIVITY

Choose an enjoyable activity:

• Walking
• Cycling
• Dancing
• Recreational sport

Duration:
20–30 minutes.


DAY 7 – REST

Take a rest day.

Optional:
Gentle walking and stretching.


SAFETY

Stop if you experience pain,
dizziness, fainting, chest pain,
or unusual shortness of breath.
"""


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str
):

    if not settings.gemini_api_key:

        return fallback_plan(
            username,
            goal,
            intensity
        )


    client = genai.Client(
        api_key=settings.gemini_api_key
    )


    prompt = f"""

{SYSTEM_SAFETY}


Create a personalized 7-day general
fitness plan.

User information:

Name: {username}

Age: {age}

Weight: {weight} kg

Goal: {goal}

Workout intensity: {intensity}


Use this exact structure:

Day 1
Day 2
Day 3
Day 4
Day 5
Day 6
Day 7


For every day include:

Warm-up

Main workout

Cool-down or recovery


For exercises provide:

• Exercise name
• Sets and repetitions
OR
• Duration
• Simple rest guidance


Include at least one recovery/rest day.

Do not prescribe extreme calorie restriction.

Do not recommend unsafe exercises.

Return only the fitness plan.
"""


    response = client.models.generate_content(

        model=settings.workout_model,

        contents=prompt
    )


    return response.text.strip()