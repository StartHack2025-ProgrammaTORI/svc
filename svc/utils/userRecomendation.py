import re
from .model import Model
from svc.plugin.consultant import repository as consultant_repository
import json

class UserRec:

    def __init__(self):
        self.model = Model()
        self.consultants = consultant_repository.consultant_list()[:20]
        self.model.append_history("system", "You are an AI that asks targeted questions to match the user with the most similar person in a given dataset.")
    
    def set_consultants(self, black_list_focus_area=None, black_list_company=None):
        self.consultants = consultant_repository.consultant_list(black_list_focus_area, black_list_company)[:20]

    def clear_history(self):
        self.model.clear_history()
        self.model.append_history("system", "You are an AI that asks targeted questions to match the user with the most similar person in a given dataset.")

    def get_next_question(self, user_responses=None):
        """Chiede all'LLM di generare una domanda basata sulle risposte dell'utente e sul dataset."""
        self.clear_history()
        system_instruction = f"""
        Your goal is to ask the user questions that help determine which person from the following dataset is most similar to them:
        
        Dataset:
        {self.consultants}

        Rules:
        - Only ask relevant questions that help distinguish between candidates.
        - Return a JSON with: "question" and "options" (3 possible options).
        """

        self.model.append_history("system", system_instruction)

        if user_responses is not None:
            for response in user_responses:
                self.model.append_history("assistant", response["question"])
                self.model.append_history("user", response["answer"])
    
        response = self.model.answer(functions=[
            {
                "name": "generate_question",
                "description": '''
                    Generates a multiple-choice question with three possible answers to help identify the user's best match. 
                    The response should contain only the question followed by three answer options, each separated by a newline character ('\n').
                    No additional text or introduction should be included—just the question and answers.
                ''',
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The main question to be presented."
                        },
                        "answers": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "minItems": 5,
                            "maxItems": 5,
                            "description": "An array containing three possible answer options."
                        }
                    },
                    "required": ["question", "answers"]
                }
            }
        ])
        if (
            response is None or 
            response.choices is None or 
            len(response.choices) == 0 or
            response.choices[0].message is None or
            response.choices[0].message.function_call is None or
            response.choices[0].message.function_call.arguments is None
        ):
            return None

        response = response.choices[0].message.function_call.arguments
        parsed_response = json.loads(response)
        question = parsed_response["question"]
        options = parsed_response["answers"]
        return {
            "question": question,
            "options": options
        }
        
    def find_best_match(self, user_responses):
        self.model.clear_history()
        system_instruction = f"""
        Your goal is to find the best match consultant using the dataset of consultants provided and the user's responses:
        
        Rules:
        - Return a JSON with: "reason" and "_id".
        
        Consultants:
        {self.consultants}
        """
        self.model.append_history("system", system_instruction)
        if user_responses is not None:
            for response in user_responses:
                self.model.append_history("assistant", response["question"])
                self.model.append_history("user", response["answer"])
        
        response = self.model.answer(  # Include the chat history
        functions=[  # Pass function definitions
            {
                "name": "best_match_consultant",
                "description": "Identifies up to four best-matching consultants from the dataset based on the user's responses and provides a brief explanation for each.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    "consultants": {
                        "type": "array",
                        "description": "A list of up to four recommended consultants with their _id and reason for selection.",
                        "items": {
                        "type": "object",
                        "properties": {
                            "_id": {
                            "type": "string",
                            "description": "The _id field of the recommended consultant."
                            },
                            "reason": {
                            "type": "string",
                            "description": "Explanation for why this consultant is a best match."
                            }
                        },
                        "required": ["_id", "reason"]
                        },
                        "maxItems": 3,
                        "minItems": 2
                    }
                    },
                    "required": ["consultants"]
                }
            }
        ],
        function_call={"name": "best_match_consultant"}
        )
        
        response = response.choices[0].message.function_call.arguments
        parsed_response = json.loads(response)
        
        return parsed_response


        


userRec = UserRec()
