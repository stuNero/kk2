from pydantic import BaseModel

class UploadResponse(BaseModel):
    rows: int
    cols: list[str]
    dtypes: dict[str, str]

class StatsResponse(BaseModel):
    stats: dict[str, dict[str,float]]
    
class AskRequest(BaseModel):
    question: str
    
class AskResponse(BaseModel):
    question: str
    answer: str
    model: str