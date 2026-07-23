

class Memory:
    """Memory storage for the agent in the present conversations. """

    # where do i store the memory? and what is the format of memory? What memeory do I want to store?
    def __init__(self):
        self.items = []

    def add(self, item: str):
        if item not in self.items:
           return self.items.append(item)

    def get_all(self):
        self.items.copy()

    def get_recent(self, n: int=5) -> list[str]:
        return self.items[-n:] if self.items else[]

    def search(self, query:str) -> list[str]:
        query = query.casefold()
        return [item for item in self.items if query in item.casefold()]

    def clean(self):
        self.items = []
    
    def __len__(self) -> int:
        return len(self.items)
    
    def __repr__(self) -> str:
        """String representation of memory. """
        return f"Memory({len(self.items)} items)"