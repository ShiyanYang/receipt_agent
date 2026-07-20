from agent import Agent

def main():
    
    model_path="./models/llama-3-8b-instruct.gguf"
    meal="Hainan Chicken"
    receipt_agent=Agent(model_path, meal)
    receipt_agent.search_pantry()
    pantry_list, answer=receipt_agent.generate_shopping_list()
    print(f"Here is my answer {answer}") 

if __name__ == "__main__":
    main()