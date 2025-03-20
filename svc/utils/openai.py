import os

class OpenAI:
    history = []

    def __init__(self):
        print('init OpenAI')
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = 'gpt-3.5-turbo'
        self.client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    def append_history(self, role, content):
        self.history.append(
            {
                "role": role,
                "content": content,
            }
        )

    def clear_history(self):
        self.history = []

    def answer(self, prompt): 
        self.history.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        return self.client.responses.create(
            model="gpt-4o-mini",
            input=self.history,
        )
        
openai = OpenAI()