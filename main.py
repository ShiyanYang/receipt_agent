from agent import Agent
import os
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        model_path = os.getenv("MODEL_PATH", "./models/llama-3-8b-instruct.gguf")
        
        if not os.path.exists(model_path):
            logger.error(f"Model file not found: {model_path}")
            sys.exit(1)
        
        logger.info(f"Agent is using {os.path.basename(model_path)}")
        receipt_agent = Agent(model_path)
        
        logger.info("Generating meal plan...")
        meal_plan = receipt_agent.generate_meal_plan()
        
        if not meal_plan:
            logger.warning("No meal plan generated")
            return
        
        logger.info("Generating shopping list...")
        shopping_list = receipt_agent.generate_shopping_list(meal_plan)
        
        print(f"\nThe shopping list is:")
        for item in shopping_list:
            print(f"  - {item}")
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)
    
if __name__ == "__main__":
    main()