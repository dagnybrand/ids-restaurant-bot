from .message import Message

class Unsure(Message):
    def to_text(self) -> str:
        return "That is outside my scope of knowledge. Please ask me a restaurant related question."