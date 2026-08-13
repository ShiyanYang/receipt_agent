
import json
import os
import logging
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class Memory:
    """Persistent memory storage for agent conversations."""

    def __init__(self, storage_file: str = "memory/conversation.json"):
        """Initialize memory with optional file persistence."""
        self.storage_file = storage_file
        self.items: List[str] = []
        self._load_from_file()

    def _ensure_storage_dir(self):
        """Ensure memory directory exists."""
        Path("memory").mkdir(exist_ok=True)

    def _load_from_file(self):
        """Load memory from persistent storage."""
        try:
            self._ensure_storage_dir()
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.items = data
                        logger.info(f"Loaded {len(self.items)} items from memory")
        except Exception as e:
            logger.warning(f"Failed to load memory from file: {e}")
            self.items = []

    def _save_to_file(self):
        """Save memory to persistent storage."""
        try:
            self._ensure_storage_dir()
            with open(self.storage_file, "w") as f:
                json.dump(self.items, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save memory to file: {e}")

    def add(self, item: str) -> bool:
        """Add item to memory if not already present."""
        if not isinstance(item, str):
            logger.warning(f"Memory item must be string, got {type(item).__name__}")
            return False
        
        if item not in self.items:
           return self.items.append(item)

    def get_all(self) -> list[str]:
        """Return all items in memory."""
        return self.items.copy()

    def get_recent(self, n: int = 5) -> list[str]:
        """Return the n most recent items."""
        if n < 0:
            raise ValueError("n must be non-negative")
        return self.items[-n:] if self.items else []

    def search(self, query: str) -> list[str]:
        """Search memory items by query string (case-insensitive)."""
        if not isinstance(query, str):
            return []
        query = query.casefold()
        return [item for item in self.items if query in item.casefold()]

    def clean(self):
        """Clear all memory items."""
        self.items = []
        self._save_to_file()
        logger.info("Memory cleaned")
    
    def __len__(self) -> int:
        """Return number of items in memory."""
        return len(self.items)
    
    def __repr__(self) -> str:
        """String representation of memory. """
        return f"Memory({len(self.items)} items)"