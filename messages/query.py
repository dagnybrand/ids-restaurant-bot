from .message import Message

class Query(Message):
    def __init__(self, text: str):
        self.text = text
    
    def to_text(self) -> str:
        return self.text
    
class RestaurantQuery(Message):
    def __init__(self, city: str | None = None, cuisine: str | None = None, limit: int | None = None):
        self.city = city
        self.cuisine = cuisine
        self.limit = limit
    
    def to_text(self) -> str:
        query_parts = []
        if self.city:
            query_parts.append(f"City: {self.city}")
        if self.cuisine:
            query_parts.append(f"Cuisine: {self.cuisine}")
        if self.limit is not None:
            query_parts.append(f"Limit: {self.limit}")
        
        return " | ".join(query_parts) if query_parts else "No specific query provided."

class ReviewQuery(Message):
    def __init__(self, restaurant_name: str | None = None, limit: int | None = None):
        self.restaurant_name = restaurant_name
        self.limit = limit
    
    def to_text(self) -> str:
        query_parts = []
        if self.restaurant_name:
            query_parts.append(f"Restaurant: {self.restaurant_name}")
        if self.limit is not None:
            query_parts.append(f"Limit: {self.limit}")
        
        return " | ".join(query_parts) if query_parts else "No specific review query provided."

class TipQuery(Message):
    def __init__(self, restaurant: str | None = None, limit: int | None = None):
        self.restaurant = restaurant
        self.limit = limit
    
    def to_text(self) -> str:
        query_parts = []
        if self.restaurant:
            query_parts.append(f"Restaurant: {self.restaurant}")
        if self.limit is not None:
            query_parts.append(f"Limit: {self.limit}")
        
        return " | ".join(query_parts) if query_parts else "No specific tip query provided."

class ExitQuery(Message):
    def to_text(self) -> str:
        return "Exiting..."
