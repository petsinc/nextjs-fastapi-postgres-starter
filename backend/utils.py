from pydantic import BaseModel

class UserRead(BaseModel):
    id: int
    name: str

class MessageCreate(BaseModel):
    content: str
    user: int

class MessageRead(BaseModel):
    id: int
    content: str
    timestamp: str
    user_id: int
    is_bot: bool


chatbot_responses = [
    "Thank you for reaching out!",
    "I'm here to help you.",
    "Can you please provide more details?",
    "I'm not sure I understand. Can you clarify?",
    "What else can I do for you?",
    "That's interesting! Tell me more.",
    "Let's see what we can do about that.",
    "I'm here to answer your questions.",
    "Could you explain that further?",
    "I’ll look into that for you.",
    "Please hold on a moment.",
    "That's a great question!",
    "I’ll need more information to help with that."
]