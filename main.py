from agent import Agent
import os 


def main():
    
    model_path="./models/llama-3-8b-instruct.gguf"
    receipt_agent = Agent(model_path)
    print(f"Agent is using {os.path.basename(model_path)}")

    receipt_agent=Agent(model_path)
    shopping_list=receipt_agent.generate_meal_plan()
    
    # need a function here to parse the output into a list

    pantry_list=receipt_agent.search_pantry()

    # need a function here to exclude what is in the pantry
    
    #print(f"The shopping list is: {final_shopping_list}")
    
if __name__ == "__main__":
    main()