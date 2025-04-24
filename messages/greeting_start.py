import random
from .message import Message

START_OPTIONS = [
    "Welcome to the Restaurant Bot! How can I assist you today?",
    "Hello! I'm here to help you with restaurant information. What would you like to know?",
    "Hi there! Ask me anything about restaurants, reviews, or tips.",
    "Greetings! What can I do for you regarding restaurants?",
    "Hello! Need help with restaurant queries? I'm here for you!",
]

class GreetingStart(Message):
    def to_text(self) -> str:
        return random.choice(START_OPTIONS)