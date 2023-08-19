from pydantic import BaseModel
from typing import Optional
from datetime import date

class Blog( BaseModel ):
    id: Optional[str] = None
    title: str
    content: str

class User( BaseModel ):
    id: Optional[str] = None
    name: str
    email_address: str
    password: str
    tagline: Optional[str] = None
    join_date: Optional[date] = date.today()



