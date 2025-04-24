import random
from .message import Message

EXIT_OPTIONS = [
    "Thank you for using the Restaurant Bot! Have a great day!",
    "It was a pleasure assisting you. Goodbye!",
    "Feel free to return if you have more questions. Take care!",
    "I hope I was able to help. Goodbye!",
    "Thanks for chatting with me. Have a wonderful day!",
]

class GreetingExit(Message):
    def to_text(self) -> str:
        return random.choice(EXIT_OPTIONS)