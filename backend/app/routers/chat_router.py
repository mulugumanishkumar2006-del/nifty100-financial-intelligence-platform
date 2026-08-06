"""
AI Chat Router
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chat_service import ask_ai

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


class ChatRequest(BaseModel):
    question: str


@router.post("/")
def chat(request: ChatRequest):
    return ask_ai(request.question)