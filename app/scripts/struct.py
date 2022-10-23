from typing import Iterable, List
from pydantic import BaseModel

class Basic_Mail(BaseModel):
    subject: str
    recipient: str
    body: str

class Text_Template(BaseModel):
    template: str
    recipient: str
    params: List[str]

class Pdf_Template(BaseModel):
    name: str
    description: str
    parameters: str
    full_text: str