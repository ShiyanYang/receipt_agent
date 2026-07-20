import json

PANTRY_FILE = "data/pantry.json"

def load_pantry():
    with open(PANTRY_FILE, "r") as f:
        try:
           data = json.load(f)
        except json.JSONDecodeError:
            return[]
        if not isinstance(data, list):
            data=[data]
        return data
    
def save_pantry(items):
    with open(PANTRY_FILE,"w") as f:
        json.dump(items, f, indent=4)

def add_item(item):
    pantry=load_pantry()
    if item not in pantry:
        pantry.append(item)
        save_pantry(pantry)

def list_items():
    return load_pantry()

def remove_item(item):
    pantry=load_pantry()
    if item in pantry:
        pantry.remove(item)
        save_pantry(pantry)
    return f"Removed {item}"