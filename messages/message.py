from abc import ABC, abstractmethod

class Message(ABC):
    
    @abstractmethod
    def to_text(self) -> str:
        pass