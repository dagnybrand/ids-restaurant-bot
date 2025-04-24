import random
from .message import Message

PROMPT_OPTIONS = [
    "What would you like to know?",
    "How else can I assist you?",
    "Is there anything else you want to ask?",
    "Do you have any other questions?",
    "How can I be of assistance?",
    "What information are you looking for?",
]

class Prompt(Message):
    def to_text(self) -> str:
        return random.choice(PROMPT_OPTIONS) 