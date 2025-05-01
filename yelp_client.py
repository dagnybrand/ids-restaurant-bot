import pandas as pd
from abc import ABC, abstractmethod


class YelpClient(ABC):
    @abstractmethod     
    def get_restaurants(self, city: str, cuisine: str, limit: int = 5) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_reviews(self, business_name: str, limit: int = 5) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_tips(self, business_name: str, limit: int = 5) -> pd.DataFrame:        
        pass