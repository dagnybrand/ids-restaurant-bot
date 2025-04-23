import os
from dotenv import load_dotenv

from gpt_client import GPTClient
from review_client import ReviewClient
from restaurant_model import RestaurantModel


class RestaurantBot:
    def __init__(self, data_dir: str, model_dir:str, gpt_api_key: str):
        self.review_client = ReviewClient(data_dir=data_dir)
        self.gpt_client = GPTClient(api_key=gpt_api_key)
        self.model = RestaurantModel()
        self.model.load(model_dir)
    
    def query(self, query: str) -> str:
        result = self.model.generate(query)
        result = result[result.find('<|start_fn|>') + len('<|start_fn|>'): result.find('<|end_fn|>')].strip()
        get, resource, args = result.split(' ', maxsplit=2)
        args = [x.strip().lstrip() for x in args.split(',') if x.strip().lstrip() != '']
        summary = "Sorry, I couldn't find any relevant information."
        if get == 'GET':
            if resource == 'RESTAURANTS':
                city = args[0]
                category = args[1]
                number = int(args[2]) if len(args) > 2 else 5
                df = self.review_client.get_restaurants(city, category, number)
                summary = self.gpt_client.summarize_businesses(df)
            elif resource == 'REVIEWS':
                restaurant = args[0]
                number = int(args[1]) if len(args) > 1 else 5
                df = self.review_client.get_reviews(restaurant, number)
                summary = self.gpt_client.summarize_reviews(df)
            elif resource == 'TIPS':
                restaurant = args[0]
                number = int(args[1]) if len(args) > 1 else 5
                df = self.review_client.get_tips(restaurant, number)
                summary = self.gpt_client.summarize_tips(df)
        
        return summary        

if __name__ == '__main__':
    load_dotenv()

    bot = RestaurantBot(
        data_dir='data/yelp',
        model_dir='jam/out-restaurant-bot',
        gpt_api_key=os.getenv("OPENAI_KEY")
    )
    while True:
        query = input("Ask me about restaurants: ")
        if query.lower() in ['exit', 'quit']:
            break
        response = bot.query(query)
        print(response)