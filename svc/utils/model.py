import os
from openai import OpenAI

class Model:
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

    def answer(self, prompt=None, functions=None, function_call=None):
        if prompt is not None:
            self.history.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )
        if functions is not None:
            print("brodooo: ",functions)
            return self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                functions=functions,
                function_call=function_call if function_call is not None else "auto"
            )
        return self.client.responses.create(
            model=self.model,
            input=self.history,
        )
