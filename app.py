from pantry import add_item, remove_item, list_items

print("Shopping Agent")
print("Type 'quit' to exit.")

while True:

    command = input("> ")

    if command == "quit":
        break

    elif command.startswith("add "):
        item = command[4:]
        print(add_item(item))

    elif command.startswith("remove "):
        item = command[7:]
        print(remove_item(item))

    elif command == "list":
        for item in list_items():
            print("-", item)

    else:
        print("Unknown command.")