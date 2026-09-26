from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session


from .crud import (
    delete_user,
    get_all_users,
    get_user,
    save_plan,
    save_user,
    update_plan
)

from .database import get_db

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .gemini_generator import (
    generate_workout_gemini
)

from .schemas import (
    UserInput,
    FeedbackRequest
)

from .updated_plan import (
    update_workout_plan
)


router = APIRouter()


templates = Jinja2Templates(

    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(

        request,

        "index.html",

        {
            "request": request,
            "error": None
        }
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(

    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)

):

    try:

        data = UserInput(

            username=username.strip(),

            user_id=user_id.strip(),

            age=age,

            weight=weight,

            goal=goal.strip(),

            intensity=intensity
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request,

            "index.html",

            {
                "request": request,

                "error":
                f"Please check your input: {exc}"
            },

            status_code=422
        )


    try:

        existing_user = get_user(

            db,

            data.user_id
        )


        if existing_user:

            user = existing_user

            user.username = data.username

            user.age = data.age

            user.weight = data.weight

            user.goal = data.goal

            user.intensity = data.intensity

            db.commit()

        else:

            user = save_user(

                db,

                data
            )


        workout_plan = generate_workout_gemini(

            data.username,

            data.age,

            data.weight,

            data.goal,

            data.intensity
        )


        nutrition_tip = (
            generate_nutrition_tip_with_flash(
                data.goal
            )
        )


        user = save_plan(

            db,

            user,

            workout_plan,

            nutrition_tip
        )


        return templates.TemplateResponse(

            request,

            "result.html",

            {

                "request": request,

                "user": user,

                "workout_plan":
                workout_plan,

                "nutrition_tip":
                nutrition_tip,

                "updated": False
            }
        )


    except Exception as exc:

        return templates.TemplateResponse(

            request,

            "index.html",

            {

                "request": request,

                "error":
                f"Generation failed: {exc}"
            },

            status_code=500
        )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)

):

    try:

        data = FeedbackRequest(

            user_id=user_id.strip(),

            feedback=feedback.strip()
        )


        user = get_user(

            db,

            data.user_id
        )


        if not user:

            return templates.TemplateResponse(

                request,

                "index.html",

                {

                    "request": request,

                    "error":
                    "User ID was not found."
                },

                status_code=404
            )


        revised_plan = update_workout_plan(

            user.original_plan,

            data.feedback,

            user.goal,

            user.intensity
        )


        user = update_plan(

            db,

            user,

            revised_plan,

            data.feedback
        )


        return templates.TemplateResponse(

            request,

            "result.html",

            {

                "request": request,

                "user": user,

                "workout_plan":
                revised_plan,

                "nutrition_tip":
                user.nutrition_tip,

                "updated": True
            }
        )


    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)
        )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db)

):

    users = get_all_users(db)


    return templates.TemplateResponse(

        request,

        "all_uswes.html",

        {

            "request": request,

            "users": users
        }
    )


@router.post(
    "/delete-user/{user_id}"
)
def remove_user(

    user_id: str,

    db: Session = Depends(get_db)
):

    success = delete_user(

        db,

        user_id
    )


    if not success:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )


    return RedirectResponse(

        "/view-all-users",

        status_code=303
    )


@router.get(
    "/api/users"
)
def api_users(

    db: Session = Depends(get_db)
):

    users = get_all_users(db)


    return [

        {

            "user_id": user.user_id,

            "username": user.username,

            "age": user.age,

            "weight": user.weight,

            "goal": user.goal,

            "intensity": user.intensity,

            "has_updated_plan":
            bool(user.updated_plan),

            "created_at":
            user.created_at.isoformat()
            if user.created_at
            else None
        }

        for user in users
    ]


@router.get(
    "/api/users/{user_id}"
)
def api_user(

    user_id: str,

    db: Session = Depends(get_db)
):

    user = get_user(

        db,

        user_id
    )


    if not user:

        raise HTTPException(

            status_code=404,

            detail="User not found"
        )


    return {

        "user_id": user.user_id,

        "username": user.username,

        "age": user.age,

        "weight": user.weight,

        "goal": user.goal,

        "intensity": user.intensity,

        "original_plan":
        user.original_plan,

        "updated_plan":
        user.updated_plan,

        "nutrition_tip":
        user.nutrition_tip,

        "feedback":
        user.feedback
    }