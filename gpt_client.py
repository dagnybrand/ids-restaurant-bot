import openai
import pandas as pd

DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant that is part of a restaurant recommendation system. Your task is to provide concise and accurate summaries of provided restaurant data. You will recieve information about restaurants, reviews, tips, user profiles, and other relevant data. Your responses should be clear and to the point, focusing on the key details that will help users make informed decisions about where to eat."

class GPTClient:
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini", system_prompt: str | None = None) -> None:
        self.client = openai.OpenAI(api_key=api_key)
        self.model_name = model_name

        if system_prompt is None:
            self.system_prompt = DEFAULT_SYSTEM_PROMPT
        else:
            self.system_prompt = system_prompt

    def ask_gpt(self, prompt: str) -> str: 
        message = [{"role":"system", "content": self.system_prompt},
                    {"role":"user", "content": prompt}]

        completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=message
        )
        
        return completion.choices[0].message.content

    def summarize_businesses(self, businesses: pd.DataFrame) -> str:
        if businesses.empty:
            return "No businesses to summarize."
        
        prompt = f"""
        Below is a table of restaurant information. Output a brief summary of each restaurant, including their names, cuisines, average ratings, and any other relevant information.

        {businesses.to_string(index=False)}
        """

        return self.ask_gpt(prompt)
    
    def summarize_reviews(self, reviews: pd.DataFrame) -> str:
        if reviews.empty:
            return "No reviews to summarize."
        
        prompt = f"""
        Below is a table of restaurant reviews. Combine the information from these reviews into a single review that highlights the overall sentiment, common themes, and any standout comments. Make sure to include both positive and negative aspects mentioned in the reviews.

        {reviews.to_string(index=False)}
        """

        return self.ask_gpt(prompt)

    def summarize_tips(self, tips: pd.DataFrame) -> str:
        if tips.empty:
            return "No tips to summarize."

        prompt = f"""
        Below is a table of tips for a restaurant. Combine the information from these tips into a single summary that captures the most useful advice and recommendations. Highlight any common themes or standout suggestions.

        {tips.to_string(index=False)}
        """

        return self.ask_gpt(prompt)
    
    def verify_input(self, q: str) -> bool:
        prompt = f"Does the following query have to do with a restuarant? Please response with YES or NO: \n {q}"

        response = self.ask_gpt(prompt)

        if "yes" in response.lower():
            return True
        elif "no" in response.lower():
            return False
        else:
            self.verify_input(q)