import json
import os
import logging
from typing import List
from pathlib import Path

logger = logging.getLogger(__name__)

PANTRY_FILE = "data/pantry.json"

def _ensure_data_dir():
    """Ensure data directory exists."""
    Path("data").mkdir(exist_ok=True)

def load_pantry() -> List[str]:
    """Load pantry items from JSON file."""
    try:
        _ensure_data_dir()
        if not os.path.exists(PANTRY_FILE):
            return []
        
        with open(PANTRY_FILE, "r") as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            logger.warning("Pantry file format invalid, expected list")
            return []
        
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse pantry file: {e}")
        return []
    except Exception as e:
        logger.error(f"Failed to load pantry: {e}")
        return []

def save_pantry(items: List[str]) -> None:
    """Save pantry items to JSON file atomically."""
    if not isinstance(items, list):
        raise TypeError("Items must be a list")
    
    try:
        _ensure_data_dir()
        # Write to temporary file first for atomicity
        temp_file = f"{PANTRY_FILE}.tmp"
        with open(temp_file, "w") as f:
            json.dump(items, f, indent=4)
        # Rename temp file to actual file
        os.replace(temp_file, PANTRY_FILE)
        logger.info(f"Saved pantry with {len(items)} items")
    except Exception as e:
        logger.error(f"Failed to save pantry: {e}")
        raise

def add_item(item: str) -> None:
    """Add an item to the pantry."""
    if not isinstance(item, str) or not item.strip():
        raise ValueError("Item must be a non-empty string")
    
    try:
        pantry = load_pantry()
        item = item.strip()
        if item not in pantry:
            pantry.append(item)
            save_pantry(pantry)
            logger.info(f"Added item: {item}")
    except Exception as e:
        logger.error(f"Failed to add item '{item}': {e}")
        raise

def list_items() -> List[str]:
    """Get all items in the pantry."""
    return load_pantry()

def remove_item(item: str) -> str:
    """Remove an item from the pantry."""
    if not isinstance(item, str) or not item.strip():
        raise ValueError("Item must be a non-empty string")
    
    try:
        pantry = load_pantry()
        item = item.strip()
        if item in pantry:
            pantry.remove(item)
            save_pantry(pantry)
            logger.info(f"Removed item: {item}")
            return f"Removed '{item}' from pantry"
        else:
            return f"Item '{item}' not found in pantry"
    except Exception as e:
        logger.error(f"Failed to remove item '{item}': {e}")
        raise