import os
from dotenv import load_dotenv

from document_planner import DocumentPlanner
from gpt_client import GPTClient
from yelp_client import YelpClient, FileYelpClient, DatabaseYelpClient
from restaurant_model import RestaurantModel
from messages import GreetingExit, Query


class RestaurantBot:
    def __init__(self, model_dir:str, gpt_api_key: str, data_dir: str | None = None) -> None:
        review_client: YelpClient = FileYelpClient(data_dir=data_dir) if data_dir is not None else DatabaseYelpClient()
        gpt_client = GPTClient(api_key=gpt_api_key)
        model = RestaurantModel()
        model.load(model_dir)

        self.document_planner = DocumentPlanner(review_client=review_client, gpt_client=gpt_client, model=model)
            

    def run(self) -> None:
        while True:
            system_msg = self.document_planner.get_next_message()
            print(system_msg.to_text())

            if type(system_msg) == GreetingExit:
                break

            user_input = input("User: ")
            self.document_planner.add_message(Query(user_input))

if __name__ == '__main__':
    load_dotenv()

    bot = RestaurantBot(
        model_dir='jam/out-restaurant-bot',
        gpt_api_key=os.getenv("OPENAI_KEY"),
        data_dir='./data/yelp'
    )
    
    bot.run()