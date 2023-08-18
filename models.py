from pydantic import BaseModel
from pydantic import field_validator
from typing import Optional

class Blog( BaseModel ):
    id: Optional[str] = None
    title: str
    content: str


