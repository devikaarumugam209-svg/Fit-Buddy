from pydantic import BaseModel, Field


class UserInput(BaseModel):

    username: str = Field(
        min_length=2,
        max_length=120
    )

    user_id: str = Field(
        min_length=1,
        max_length=80
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=20,
        lt=400
    )

    goal: str = Field(
        min_length=2,
        max_length=80
    )

    intensity: str = Field(
        pattern="^(low|medium|high)$"
    )


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=1,
        max_length=80
    )

    feedback: str = Field(
        min_length=3,
        max_length=2000
    )