import pandas as pd
from enum import Enum
from .message import Message

class QueryType(Enum): 
    RESTAURANT = "restaurant"
    REVIEW = "review"
    TIP = "tip"
    EXIT = "exit"

class Response(Message):
    def __init__(self, data: pd.DataFrame, text: str, query_type: QueryType):
        self.data = data
        self.text = text
        self.query_type = query_type

    def to_text(self) -> str:
        return self.text