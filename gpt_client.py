import openai

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