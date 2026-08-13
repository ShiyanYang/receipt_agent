from pantry import add_item, remove_item, list_items
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def print_help():
    print("\nAvailable commands:")
    print("  list              - Show all pantry items")
    print("  add <item>        - Add item to pantry")
    print("  remove <item>     - Remove item from pantry")
    print("  quit              - Exit the application\n")

def main():
    print("Shopping Pantry Manager")
    print_help()
    
    try:
        while True:
            try:
                command = input("> ").strip()
                
                if not command:
                    continue
                    
                if command.lower() == "quit":
                    print("Goodbye!")
                    break
                    
                elif command.lower() == "list":
                    items = list_items()
                    if not items:
                        print("Pantry is empty")
                    else:
                        print("Pantry items:")
                        for item in items:
                            print(f"  - {item}")
                    
                elif command.lower().startswith("add "):
                    item = command[4:].strip()
                    if not item:
                        print("Error: Please specify an item to add")
                    else:
                        try:
                            add_item(item)
                            print(f"Added '{item}' to pantry")
                        except Exception as e:
                            logger.error(f"Failed to add item: {e}")
                            print(f"Error: Could not add item")
                    
                elif command.lower().startswith("remove "):
                    item = command[7:].strip()
                    if not item:
                        print("Error: Please specify an item to remove")
                    else:
                        try:
                            result = remove_item(item)
                            print(result)
                        except Exception as e:
                            logger.error(f"Failed to remove item: {e}")
                            print(f"Error: Could not remove item")
                    
                elif command.lower() == "help":
                    print_help()
                    
                else:
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                print(f"Error: {e}")
                
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()