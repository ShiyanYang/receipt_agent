from agent import Agent
import os 


def main():
    
    model_path="./models/llama-3-8b-instruct.gguf"
    receipt_agent = Agent(model_path)
    print(f"Agent is using {os.path.basename(model_path)}")

    print("Hi, I am your shoppling assistance. Could you please tell me what dishes you want to cook this week? ")

    while True:
        conversation = input("> ")
        # make this into a cli conversation
        if 'exit' not in conversation: 
            receipt_agent=Agent(model_path)
            receipt_agent.search_pantry()
            answer=receipt_agent.generate_shopping_list(conversation)
            print(f"Here is my answer {answer}") 
        else:        
            break

if __name__ == "__main__":
    main()