import openai

DEFAULT_SYSTEM_PROMPT = "Think critically about the following."

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