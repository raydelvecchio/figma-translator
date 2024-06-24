from pydantic import BaseModel
from typing import Any, Dict

class FigmaImageResponse(BaseModel):
    err: Any
    images: Dict[str, str]
