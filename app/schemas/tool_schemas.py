from pydantic import BaseModel

class MemorySearchInput(BaseModel):
    namespace: str
    query: str
    k: int = 5
