
from llama_cpp import Llama
from pantry import list_items
from memory import Memory
import json

class Agent:
    """
    An AI agent that can generate the missing ingradients as shopping list.
    """

    def __init__(self, model_path: str):
        """Initialize the agent. """
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )
        self.pantry_list= None
        self.memory = Memory()
        self.tools = [{
                "type": "function",
                "function": {
                    "name": "update_shopping_list",
                    "description": "Add missing grocery items to the shopping list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "new_items": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of missing ingredients/items"
                            }
                        },
                        "required": ["new_items"]
                    }
                }
            }]

    def search_pantry(self):
        items = list_items()
        if not items:
            self.pantry_list="nothing"
        else:
            self.pantry_list = items
    

    def generate_meal_plan(self):
        
        system_prompt = f"""You role is to assistant the user for meal planning and generate the shopping list.

        CRITICAL INSTRUCTIONS: 
        1. The first question is always about the number of days for meal planning.
        2. Your need to deeply understand the user's needs and feelings.
        3. You either ask a follow-up question or generate the meal plan.
        4. Once you have enough information, generate a meal plan for each day.
        5. In the end, generate the shopping list based on the meal plan.
        
        Response about meal plan (markdown table only; first column: day, second column: breakfast, lunch, or dinner, third colum: the name of the mean, fourth column: ingredients)
        Response about shopping list (JSON format only)
        Require JSON format:
        {{"Output": "Shopping Item", "Category":"the category of ingredients", "Shopping List": "the items of ingredients"}}
        """
        print("Hi I am your meal planning buddy. How many days do you want me to prepare for your meal?")
        
        response=""
        messages = [
            {"role":"system", "content": system_prompt}
            ]
         
        while True:  
            user_input = input ("You: ")
            if user_input.strip().lower() in ('exit','quit','bye'):
                print("See you next time : )")
                break
            
            messages.append({"role":"user","content": user_input})
            
            try:
                response = self.llm.create_chat_completion(
                    messages = messages,
                    temperature = 0.0,
                    max_tokens = 1024,
                ) 
                response = response["choices"][0]["message"]["content"].strip()
                print(f"Answer: {response}")
                if "Output" in response and "Category" in response and "Shopping List" in response:
                   shopping_list=response
                messages.append({"role": "assistant", "content": response})
                
            except (KeyError, IndexError, AttributeError) as e:
                    print('Create_chat_completion is not available ')
                    raise e
            
        return shopping_list