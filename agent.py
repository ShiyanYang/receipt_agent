
from llama_cpp import Llama
from pantry import list_items

class Agent:
    """
    An AI agent that can generate the missing ingradients as shopping list.
    """

    def __init__(self, model_path: str, meal: str):
        """Initialize the agent. """
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            verbose=False
        )
        self.meal= meal
        self.pantry_list= None

    def search_pantry(self):
        items = list_items()
        if not items:
            self.pantry_list="nothing"
        else:
            self.pantry_list = items
        
        
    def generate_shopping_list(self):
        response=self.llm.create_chat_completion( # a chat completion is an api format with a list of messages. How does this related to mcp?
            # make this messages into plannings
            messages=[
                {"role": "system", "content":"you are a chief helping housewife prepare dinner."},
                {"role":"user","content": f"I plan to cook {self.meal}."},
                {"role":"user", "content":f"Now, I have {self.pantry_list} in my pantry."},
                {"role":"user", "content":"What is missing in the pantry that I need to buy."}
            ],
            max_tokens=512,
            temperature=0
        )
        
        print(f"This is what I have in the pantry: {self.pantry_list}")
        answer = response["choices"][0]["message"]["content"]
        
        return self.pantry_list, answer