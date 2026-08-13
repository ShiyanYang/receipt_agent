
from llama_cpp import Llama
from pantry import list_items
from memory import Memory
from config import config
import json
import re
import logging
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)

class Agent:
    """AI agent generates the shopping list."""

    def __init__(self, model_path: str):
        """Initialize the agent with model and configuration."""
        self.llm = Llama(
            model_path=model_path,
            n_ctx=config.LLM_N_CTX,
            n_threads=config.LLM_N_THREADS,
            verbose=False
        )
        self.pantry_list = None
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
        
    def search_pantry(self) -> Optional[List[str]]:
        """Search and cache pantry items."""
        try:
            items = list_items()
            self.pantry_list = items if items else []
            return self.pantry_list
        except Exception as e:
            logger.error(f"Failed to search pantry: {e}")
            return []
    

    def generate_meal_plan(self):
        """Generate the meal plan over the next X days."""
        
        system_prompt = """You role is to assistant the user for meal planning.

        CRITICAL INSTRUCTIONS: 
        1. The first question is always about the number of days for meal planning.
        2. Your need to understand the user's needs.
        3. After each question, your next response is either a follow-up question or the meal plan.
        4. The meal plan response is a ONLY JSON format. It must follow the following schema. 
    '''
    [
      {"day": "Day 1", "meal_type": "breakfast", "meal_name": "...", "ingredients": ["...", "..."]},
      {"day": "Day 1", "meal_type": "lunch", "meal_name": "...", "ingredients": ["...", "..."]}
    ]
    '''
        """

        print("Hi I am your meal planning assistant. How many days do you want to prepare for meals?")
        meal_plan = None
        response="" # create an empty response first

        messages = [
            {"role":"system", "content": system_prompt}
            ]
         
        while True:  
            user_input = input ("You: ")
            if user_input.strip().lower() in ('exit','quit','bye'):
                print("See you next time : )")
                break
            
            messages.append({"role":"user","content": user_input})
            # 💾 Save user input to persistent memory
            self.memory.add(f"User: {user_input}")
            
            try:
                response = self.llm.create_chat_completion(
                    messages=messages,
                    temperature=config.LLM_TEMPERATURE,
                    max_tokens=config.LLM_MAX_TOKENS,
                ) 
                content = response["choices"][0]["message"]["content"].strip()
                
            except (KeyError, IndexError, AttributeError) as e:
                    print('Create_chat_completion is not available ')
                    raise e
            
            print(f"Answer:{content}")
            messages.append({"role":"assistant", "content":content})
            # 💾 Save assistant response to persistent memory
            self.memory.add(f"Assistant: {content}")    

            candidate = content.strip()
            
            try:
                match = re.search(r'\[\s*\{.*?\}\s*\]', candidate, re.DOTALL)

                if match:
                    parsed = json.loads(match.group())
                    if isinstance(parsed, list) and all(
                        isinstance(item, dict) and {"day", "meal_type", "meal_name", "ingredients"} <= item.keys()
                        for item in parsed
                    ):
                        meal_plan = parsed
                        print("Meal plan generated.")
                        break
                
            except (json.JSONDecodeError, TypeError):
                pass
               
        return meal_plan
    
    def _normalize(self, item: str) -> str:
        """Lowercase and strip whitespace/punctuation so 'Tomato', 'tomato ', 'Tomatoes' compare cleanly."""
        if not isinstance(item, str):
            raise TypeError(f"Expected string, got {type(item).__name__}")
        return item.strip().lower()

    def _flatten_ingredients(self, meal_plan: List[Dict[str, Any]]) -> List[str]:
        """Turn the meal plan into a flat list of ingredient entries."""
        if not isinstance(meal_plan, list):
            raise TypeError(f"Expected list, got {type(meal_plan).__name__}")
        
        all_ingredients = []
        for meal in meal_plan:
            ingredients = meal.get("ingredients", [])
            if isinstance(ingredients, list):
                all_ingredients.extend(ingredients)
        return all_ingredients
    
    def _filter_out_pantry_items(self, ingredients: List[str], pantry_list: Optional[List[str]]) -> List[str]:
        """Remove ingredient entries that are already available in the pantry."""
        if not isinstance(ingredients, list):
            raise TypeError(f"Expected list, got {type(ingredients).__name__}")
        
        pantry_list = pantry_list or []
        pantry_set = {self._normalize(item) for item in pantry_list if isinstance(item, str)}
        
        filtered_ingredients = []
        seen = set()
        for entry in ingredients:
            if isinstance(entry, str):
                normalized = self._normalize(entry)
                if normalized not in pantry_set and normalized not in seen:
                    filtered_ingredients.append(entry)
                    seen.add(normalized)
        
        return filtered_ingredients
    
    
    def generate_shopping_list(self, meal_plan: Optional[List[Dict[str, Any]]]) -> List[str]:
        """Generate the shopping list that is not in the pantry."""
        if meal_plan is None:
            logger.warning("No meal plan provided")
            return []
        
        try:
            all_ingredients = self._flatten_ingredients(meal_plan)
            pantry_list = self.search_pantry()
            needed = self._filter_out_pantry_items(all_ingredients, pantry_list)
            
            if not needed:
                logger.info("All ingredients available in pantry")
                return []
            
            logger.info(f"Generated shopping list with {len(needed)} items")
            return needed
        except Exception as e:
            logger.error(f"Failed to generate shopping list: {e}")
            raise