
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
        
        
    def generate_shopping_list(self, meal: str):
        try:
            response=self.llm.create_chat_completion( # a chat completion is an api format with a list of messages. How does this related to mcp?
                # make this messages into plannings
                messages=[
                    {"role": "system", "content":"you are a chief helping housewife prepare dinner."},
                    {"role":"user","content": f"I plan to cook {meal}."},
                    {"role":"user", "content":f"Now, I have {self.pantry_list} in my pantry."},
                    # insert memory into the message
                    #{"role":"system", "content":f"This is what is already in the shopping list: {self.memory.get_all()}"}, 
                    {"role":"user", "content":"What are the new items that I need to put into my shopping list?"}
                ],
                max_tokens=512,
                temperature=0,
                # how can i reliabley control the format of the output only as the list of shopping items?
                tools=self.tools, # trying to control the format of the output
                tool_choice={"type":"function", "function":{"name":"update_shopping_list"}}
            )
            
            tool_call = response["choices"][0]["message"]["tool_calls"][0]
        
            args=json.loads(tool_call["function"]["arguments"])
            print(args)
            if self.memory:
                self.memory.add(args['new_items'])
        
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            print(f"⚠️ Error in generate_shopping_list: {e}")
            return []
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            return [] 
        
        return args["new_items"]