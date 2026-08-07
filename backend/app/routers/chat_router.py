"""
AI Chat Router

Handles AI-powered financial chat requests.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.chat_service import ask_ai


router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


# ==========================================================
# Request Schema
# ==========================================================

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Financial question asked by the user.",
    )


# ==========================================================
# AI Chat Endpoint
# ==========================================================

@router.post("/")
def chat(request: ChatRequest):
    """
    Process a financial question using the AI chat service.
    """

    try:
        question = request.question.strip()

        if not question:
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty.",
            )

        result = ask_ai(question)

        return result

    except HTTPException:
        raise

    except Exception as exc:
        print(f"❌ AI Chat Error: {exc}")

        raise HTTPException(
            status_code=500,
            detail="Unable to generate AI response.",
        )