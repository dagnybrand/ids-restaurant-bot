from gpt_client import GPTClient
from yelp_client import YelpClient
from restaurant_model import RestaurantModel
from messages import Message, GreetingStart, GreetingExit, Query, ExitQuery, Response, RestaurantQuery, ReviewQuery, TipQuery, QueryType, Unsure

class DocumentPlanner:
    def __init__(self, review_client: YelpClient, gpt_client: GPTClient, model: RestaurantModel):
        self.review_client = review_client
        self.gpt_client = gpt_client
        self.model = model

        self.curr_restaurant_list = None
        self.curr_restaurant = None
        self.curr_city = None

        self.messages: list[Message] = []
    
    def __format_query(self, query: str) -> str:
        return f"QUERY:\n{query}\nRESPONSE:\n"
    
    def parse_query(self, query: str) -> Message | None:
        if query.strip().lower() in ['exit', 'quit']:
            return ExitQuery()
        
        result = self.model.generate(self.__format_query(query))

        result = result[result.find('<|start_fn|>') + len('<|start_fn|>'): result.find('<|end_fn|>')].strip()
        get, resource, args = result.split(' ', maxsplit=2)
        args = [x.strip().lstrip() for x in args.split(',') if x.strip().lstrip() != '']
        if get == 'GET':
            if resource == 'RESTAURANTS':
                city = args[0]
                category = args[1]
                number = int(args[2]) if len(args) > 2 else 5
                return RestaurantQuery(city=city, cuisine=category, limit=number)
            elif resource == 'REVIEWS':
                restaurant = args[0]
                number = int(args[1]) if len(args) > 1 else 5
                return ReviewQuery(restaurant_name=restaurant, limit=number)
            elif resource == 'TIPS':
                restaurant = args[0]
                number = int(args[1]) if len(args) > 1 else 5
                return TipQuery(restaurant=restaurant, limit=number)
        
        return None

    def add_message(self, message: Message):
        if type(message) == Query:
            message = self.parse_query(message.to_text())

        self.messages.append(message)

    def get_next_message(self) -> Message:
        next_message = None

        last_message = self.messages[-1] if self.messages else None
        if len(self.messages) == 0:
            next_message =  GreetingStart()
        elif type(last_message) == RestaurantQuery:
            restaurants = self.review_client.get_restaurants(last_message.city, last_message.cuisine, last_message.limit)
            self.curr_restaurant_list = restaurants
            self.curr_city = last_message.city
            summary = self.gpt_client.summarize_businesses(restaurants)
            next_message = Response(data=restaurants, text=summary, query_type=QueryType.RESTAURANT)
        elif type(last_message) == ReviewQuery:
            reviews = self.review_client.get_reviews(last_message.restaurant_name, last_message.limit)
            self.curr_restaurant = last_message.restaurant_name
            summary = self.gpt_client.summarize_reviews(reviews)
            next_message = Response(data=reviews, text=summary, query_type=QueryType.REVIEW)
        elif type(last_message) == TipQuery:
            tips = self.review_client.get_tips(last_message.restaurant, last_message.limit)
            self.curr_restaurant = last_message.restaurant
            summary = self.gpt_client.summarize_tips(tips)
            next_message = Response(data=tips, text=summary, query_type=QueryType.TIP)
        elif type(last_message) == ExitQuery:
            next_message = GreetingExit()
        elif type(last_message) == Unsure:
            next_message = Unsure()
        
        self.messages.append(next_message)

        return next_message

        