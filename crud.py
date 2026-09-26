from sqlalchemy.orm import Session

from .models import User


def save_user(
    db: Session,
    data
):

    user = User(

        user_id=data.user_id,

        username=data.username,

        age=data.age,

        weight=data.weight,

        goal=data.goal,

        intensity=data.intensity,

        original_plan="",

        nutrition_tip=""
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def save_plan(
    db: Session,
    user: User,
    plan: str,
    tip: str
):

    user.original_plan = plan

    user.nutrition_tip = tip

    db.commit()

    db.refresh(user)

    return user


def update_plan(
    db: Session,
    user: User,
    revised_plan: str,
    feedback: str
):

    user.updated_plan = revised_plan

    user.feedback = feedback

    db.commit()

    db.refresh(user)

    return user


def get_user(
    db: Session,
    user_id: str
):

    return (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )


def get_original_plan(
    db: Session,
    user_id: str
):

    user = get_user(
        db,
        user_id
    )

    if user:
        return user.original_plan

    return None


def get_all_users(
    db: Session
):

    return (
        db.query(User)
        .order_by(
            User.created_at.desc()
        )
        .all()
    )


def delete_user(
    db: Session,
    user_id: str
):

    user = get_user(
        db,
        user_id
    )

    if not user:
        return False

    db.delete(user)

    db.commit()

    return True